Observer 是 `ParkingControllerNew` 内部的运行状态观测层，用于把车辆状态、轨迹执行状态、碰撞决策、机械库位上下文等信息加工成更高层的控制辅助状态，给 `ParkingControllerNew` 的状态切换、段执行、扭矩转换提供判断条件。

核心作用：

- 识别溜车、卡滞、大扭矩过冲等异常或风险状态
- 估计加速度，用于机械库位扭矩控制
- 识别机械库位坡道阶段，用于加速度、jerk、扭矩和坡度补偿

# 1. Observer 初始化

`ParkingControllerNew::Initialize(...)` 中创建 Observer：

```cpp
observer_ =
    std::make_unique<Observer>(ap_control_cmd_config_, vehicle_calibration);
```

`Observer` 构造函数注册 5 个组件：

| 组件 | 名称 | 优先级 | 文件 |
| --- | --- | --- | --- |
| `SlipMonitor` | `slip_monitor` | HIGH | `slip_monitor.*` |
| `LargeTorqueMonitor` | `large_torque_monitor` | HIGH | `large_torque_monitor.*` |
| `StuckMonitor` | `stuck_monitor` | HIGH | `stuck_monitor.*` |
| `AccEstimator` | `acc_estimator` | LOW | `acc_estimator.*` |
| `StereoObserver` | `stereo_observer` | LOW | `stereo_observer.*` |

`AddComponent(...)` 会：

1. 调用组件 `Init(params_, vehicle_params_)`。
2. 在组件内部初始化 `fields_map_`。
3. 放入 `components_` map。
4. 按优先级排序 `components_with_priority_`。

更新顺序由优先级决定，当前 HIGH 组件先更新，LOW 组件后更新。

# 2. `ObserverComponent` 基类

所有组件继承 `ObserverComponent`。

关键接口：

- `Init(...)`
  - 保存配置与车辆标定。
  - 调用 `InitFieldsMap()` 初始化可读字段。
- `CheckConditions(...)`
  - 判断当前帧是否满足组件更新条件。
- `Update(...)`
  - 组件主更新逻辑。
- `UpdateFieldsMap()`
  - 把成员变量同步到 `fields_map_`。
- `AssignDebugInfo(...)`
  - 把组件内部状态写到 debug 。
- `Reset()`
  - 重置组件状态。
- `ResetBySegment()`
  - 段切换时重置组件状态。

组件输出全部保存在`FieldsMap` ：

```cpp
std::unordered_map<std::string, Result> fields_map_;
```

`Result` 是一个类型擦除容器，可以存储不同类型字段：

```text
bool
int
double
StereoStage
...
```
# 3. Reset 时机

Observer 有三类 reset：

## 3.1 全量 reset

`observer_->Reset()` 会 reset 所有组件，并清除 `Observer` 自身异常标记。

在 `ParkingControllerNew::ResetControlParamsByParking(...)` 中调用。即一次泊车任务重置时，所有 observer 状态被清空。

## 3.2 按 segment reset

`observer_->ResetBySegment()` 会调用各组件 `ResetBySegment()`。

在 `ParkingControllerNew::InitSegmentFlag()` 和 `ResetControlParamsBySegment(...)` 中使用。当前实现里：

- `StuckMonitor::ResetBySegment()` 会清空 stuck 状态。
- `LargeTorqueMonitor::ResetBySegment()` 会清空 overstop/overspeed/exit 等状态。
- 其他组件默认不处理，或只在 `Reset()` 中处理。

## 3.3 单组件 reset

`observer_->Reset(component_name)` 只 reset 指定组件。

当前使用点：

- `switch_parking_has_velocity_` 时 reset `stuck_monitor`。
- `StopEmergencyIfExceedEndPoint(...)` 触发后 reset `large_torque_monitor`。

# 4. Observer 调度逻辑

逻辑链路：

```text
ParkingControllerNew
	-> observer_->Update(UpdateObserverInput(data_manager))，每个状态机的handle函数开头都会执行
		-> UpdateObserver(observer_input)
			-> 保存 vehicle_state_
		-> UpdateComponent(observer_input)
			-> 按优先级遍历 components_with_priority_
			-> component->Update(observer_input)
				-> CheckConditions() 规定工作范围
				-> 主体逻辑
				-> UpdateFieldsMap() 更新 fields_map_
	-> ParkingControllerNew 通过 observer_->Get<T>(component, field) 读取
	-> ParkingControllerNew通过observer::AssignDebugInfo(...)，按组件顺序调用各组件 `AssignDebugInfo(...)`来设置debug信息
```

# 5. 获取数据

现有 component 都注册在 `observer` 内部，在每个控制周期会自动更新。控制层可以通过统一接口访问目标数据：

```cpp
observer_->Get<type>(Component::component_name, data_field_name);
```

其中：

- `type`：目标字段的数据类型
- `Component::component_name`：目标 component 名称
- `data_field_name`：目标字段名称

读取流程：

```text
1. Observer 在 components_ 中查找 component name
2. 调用 component->Get<T>(field)
3. component 在 fields_map_ 中查找 field
4. Result 按 T 类型取值
5. 成功则返回字段值
6. component 不存在、field 不存在或类型错误时：
   - 记录错误日志
   - observer is_abnormal_ = true，然后走异常退出流程
   - 返回 T{} 默认值
```

因此 observer 的读取是“按字符串字段名 + 模板类型”完成的，字段名和类型必须和 component 注册保持一致。

# 6. 新增组件

如果需要新增 component，按以下步骤接入。

## 6.1 在 `observer_component.h` 中新增 component 名称

在 `Component{}` 中新增 `component_name`：

```cpp
inline static const std::string new_component = "component_name";
```

## 6.2 在 `observer.cc` 构造函数中注册 component

在 `Observer` 构造函数中添加新 component：

```cpp
AddComponent(std::make_unique<Component>(component_name, Priority));
```

## 6.3 添加 component 头文件和实现文件

新增：

- `new_component.h`
- `new_component.cc`

## 6.4 在 `CheckConditions` 中设计运行范围

在 `new_component.cc` 的 `Component::CheckConditions(observer_input)` 函数中设计 component 的运行范围。

该函数用于判断当前控制周期是否需要执行该 component 的更新逻辑。

## 6.5 在 `InitFieldsMap` 中初始化目标数据

在 `Component::InitFieldsMap()` 中对目标数据进行初始化：

```cpp
fields_map_["field_name"] = Result(field_data);
```

## 6.6 在 `UpdateFieldsMap` 中更新目标数据

在**主体逻辑**之后需要 `Component::UpdateFieldsMap()` 中对目标数据进行更新：

```cpp
bool success = UpdateResults(
    fields_map_,
    std::make_pair("field_name", field_data));
```

`UpdateFieldsMap()` 中写入的字段，需要与 `InitFieldsMap()` 中初始化的字段保持一致，否则后续通过 `observer_->Get(...)` 读取时可能失败。

# 7. 组件介绍

## 7.1 `SlipMonitor`

### 7.1.1 输出字段

`fields_map_`：

- `is_sliping`：核心变量，判断当前是否处于溜车状态
- `is_sliping_static`：判断是否处于溜车后刹停静止状态
- `slip_static_counter`：溜车后刹停静止时间计数
- `sliping_counter`：溜车次数计数
- `slip_back_holding_flag`：同`is_sliping_static`
- `accumulated_movement`：累积溜车位移

### 7.1.2 更新条件

`SlipMonitor` 没有重写 `CheckConditions()`，因此默认总是允许更新。

如果是第一帧，只记录当前位置并返回。

### 7.1.3 核心逻辑

`SlipMonitor` 用车辆当前位置差分计算车体纵向位移：

```text
longitudinal_movement =
  delta_x * cos(heading) + delta_y * sin(heading)
```

再乘以当前期望档位：

```text
movement_error = longitudinal_movement * expected_gear
speed = linear_velocity * expected_gear
```

含义：

- `movement_error > 0` 表示沿期望方向移动
- `movement_error < 0` 表示相对期望方向后退
- `speed > 0` 表示沿期望方向移动
- `speed < 0` 表示相对期望方向后退

如果 `movement_error > 0.01` 或 `speed > 0.07`，清零累计后退量。否则累计：

```text
accumulated_movement += movement_error
```

触发 `is_sliping_` 的条件：

- 当前不是 `SEGMENT_SWITCH_GEAR_WITHOUT_STOP`。
- 当前还没处于 slipping。
- 满足速度或距离后退：
  - `speed < -speed_threshold`
  - 或 `accumulated_movement < -0.055`
- 同时满足坡度/机械库位条件：
  - 目标为机械库位且车尾距离入口线小于 `-3.0`
  - 或 `abs(pitch) > sliping_pitch_threshold_`（这里有点问题，`sliping_pitch_threshold_`已经改成0了，表示这个条件始终会被满足，机械库位的条件实际上已经没有意义了）

`SEGMENT_SWITCH_STARTUP` 下速度阈值提高到 `0.2`，其他阶段默认 `0.07`。

触发 slipping 后：

- 如果车辆完全停住，且本帧后退量不明显，`slip_static_counter_++`。
- 如果 `slip_static_counter_ > 10`：
  - `slip_back_holding_flag_ = true`
  - `is_sliping_ = false`
  - `is_sliping_static_ = true`
  - `sliping_counter_++`
  - 记录 `slip_origin_pos_`

如果之后车辆离开 slip origin 超过 `0.5m`，清零 `sliping_counter_`。

### 7.1.4 Controller 使用点

`ParkingControllerNew` 中直接使用：

- `GetSlipingCounter()`：读取 `slip_monitor.sliping_counter`，大于3表示在同一位置连续溜车3次，会跳转到`AbnormalStoppingState`，走异常退出流程
- `is_sliping_static()`：读取 `slip_monitor.is_sliping_static`，用于重规划请求
- `ConvertToTorque(...)`：`setSlipingFlag(observer_->Get<bool>(slip_monitor, "is_sliping"))`，如果 slipping，`TorqueController` 会强制目标扭矩到较大负扭矩。

## 7.2 `StuckMonitor`

### 7.2.1 输出字段

`fields_map_`：

- `is_stuck`：表示车辆运动过程中被卡停，会重规划
- `is_startup_stuck`：表示车辆起步过程中被卡停，会走异常退出流程

### 7.2.2 更新条件

`CheckConditions(...)` 要求只有处于以下APA 状态才会运行：

- `STATE_RUNNING`
- `STATE_RPA_MOVING_RUNNING`
- `STATE_MANEUVERING_RUNNING`

不满足时会 `Reset()` 并返回。

### 7.2.3 核心逻辑

先计算剩余距离：

```text
rest_distance = epoint.end_y_error * segment.gear
```

分阶段判断：

- `SEGMENT_EMERGENCY_STOPPING` 或 `SEGMENT_STOPPING`
  - 如果车辆完全停止且 `rest_distance < -0.15`，认为 `is_stuck_ = true`。
- `SEGMENT_STARTUP` 或 `SEGMENT_SWITCH_STARTUP`
  - 调用 `IsVehicleStuck(10s)`，超过 10 秒完全静止则 `is_startup_stuck_ = true`。
- `SEGMENT_TRACKING`
  - 调用 `IsVehicleStuck(8s)`，超过 8 秒完全静止则 `is_stuck_ = true`。

`IsVehicleStuck(...)` 使用 `vehicle_state.pose_timestamp` 计算连续静止时间：

- 如果当前未记录 stuck timestamp，则记录第一帧静止时间。
- 如果车辆完全停止，则持续更新时间；否则清零。
- 超过阈值返回 true。

### 7.2.4 Controller 使用点

- `ParkingControllerNew::is_stuck()`：用于重规划
- `ParkingControllerNew::startup_stuck()`：起步卡停，异常退出
- `ExecuteSegment(...)`：`switch_parking_has_velocity_` 场景会单独 reset `stuck_monitor`。
- `ApaExecuteTrackingStage(...)`：如果 tracking 中 `is_stuck`，当前 segment 直接进入 `SEGMENT_FINISHED`。
- `ConvertToTorque(...)`：`torque_controller_->setStuckFlag(is_stuck)`，本来是准备被卡住的时候可以调整扭矩增加速度来减少被卡的时间预留的接口，但现在没做

## 7.3 `LargeTorqueMonitor`

### 7.3.1 输出字段

`fields_map_`：

- `overspeed_flag`：超速标志位，最弱一级，只需要控速
- `large_torque_overstop_flag`：大扭矩超停，中间级，需要快速刹停
- `large_torque_exit_flag`：扭矩过大，剩余距离不够，异常退出，最高级
- `exit_overstop_flag`：大扭矩超停后，会执行急刹，满足某些条件后会回到正常状态，表示切换标志位
- `acc_predicted`：当前实时扭矩换算的加速度
- `stop_distance_by_torque`：当前实时扭矩预测出来的刹停距离

### 7.3.2 更新条件

`CheckConditions(...)` 要求：

- 当前 APA 状态属于以下之一：
	  - running 类状态
	  - `STATE_ABNORMAL_STOPPING`
	  - `STATE_ABNORMAL_PULL_P_GEAR`
	  - `STATE_ABNORMAL_COMPLETE`
	  - `STATE_GOAL_STOPPING`
	  - `STATE_PULL_P_GEAR`
	  - `STATE_COMPLETE`
	  - `STATE_WAIT_PLANNER`
- 不在进入机械库位阶段：`!is_enter_stereo_lot_`
- 当前 segment stage 不是：
	  - `SEGMENT_SWITCH_STARTUP`
	  - `SEGMENT_SWITCH_GEAR_WITHOUT_STOP`

不满足时 `Reset()`。

### 7.3.3 核心逻辑

该组件用当前实际轮端扭矩预测停车距离，并检测大扭矩导致的过冲/超速风险。

`ComputeDistanceByTorque(...)`：

- 如果 `abs(wheel_torque) < 500`，返回 0。
- 用 `vehicle_model_ptr_->ComputeAcc(data_manager, abs(wheel_torque))` 估计当前扭矩对应加速度。
- 假设延迟 `0.25s`。
- 假设后续用 `large_torque_stopping_jerk = 6.0` 拉到 `large_torque_stopping_acc = -2.0`。
- 根据 jerk 和速度积分估算停车距离。

`Update(...)` 中还计算：

- `planned_speed = abs(epoint.planned_speed)`
- `cur_speed = abs(vehicle_state.linear_velocity())`
- `speed_threshold = clamp(planned_speed * 1.25, 0.1, 1.0)`
- `rest_stop_distance = -epoint.end_y_error * segment.gear`
- `acc_predicted = vehicle_model.ComputeAcc(data_manager, vehicle_torque)`

其中 `vehicle_torque` 取 wheel torque 和 BCS torque 中绝对值更大的那个。

触发逻辑：

- `large_torque_exit_flag_`
  - 当前低速接近静止。
  - `acc_predicted > 1.0`。
  - `stop_distance_by_torque_ > rest_stop_distance * 1.25`。
- `large_torque_overstop_flag_`
  - `stop_distance_by_torque_ > rest_stop_distance`。
  - `acc_predicted > 1.0`。
  - 当前速度大于规划速度。
- `overspeed_flag_`
  - 当前速度大于 `speed_threshold`。
  - 当前速度大于 `0.5`。
  - `acc_predicted > 0.5`。
- 退出 overstop/overspeed
  - 已经触发 overstop 或 overspeed。
  - BCS torque 有制动。
  - 当前速度低于规划速度，或规划速度和当前速度都接近 0。


### 7.3.4 Controller 使用点

`LargeTorqueMonitor` 对控制影响很直接：

- `ExecuteSegment(...)`：如果 `large_torque_overstop_flag` 且当前 stage 为 `SEGMENT_STARTUP` 或 `SEGMENT_STOPPING`，强制切到 `SEGMENT_TRACKING`，这是因为此时车辆可以会因为控速或者急刹被刹停，而只有`SEGMENT_TRACKING`是闭环控制，能够让车辆自然再次起步
- `ApaExecuteTracking(...)`
  - `large_torque_overstop_flag` 成立时，目标加速度压到 `large_torque_stopping_acc_`。
  - 使用 `large_torque_stopping_jerk_` 做加速度限幅。
  - `exit_overstop_flag` 成立时，`previous_target_acc_mpss_ = 0.0`，快速取消刹车
- `ApaExecuteObstacleTracking(...)`
  - 类似地压低 `command_acc` 并提高 jerk 约束。
- `ConvertToTorque(...)`
  - `large_torque_overstop_flag || overspeed_flag` 写入 `TorqueControllerInput.is_crossing_over_`，会快速卸掉扭矩，并放大扭矩斜率
  - `is_creep_` 判断要求 `large_torque_overstop_flag` 和 `overspeed_flag` 都为 false。
- `is_running_abnormol()`
  - `large_torque_exit_flag` 会触发 running abnormal，从而跳转到异常退出流程
- `ApaExecuteTrackingStage(...)`
  - `StopEmergencyIfExceedEndPoint(...)` 成立时会 reset `large_torque_monitor`。

## 7.4 `AccEstimator`

### 7.4.1 输出字段

`fields_map_`：

- `speed_estimated`：滑模微分器观测得到的速度
- `acc_estimated`：滑模微分器观测得到的加速度

### 7.4.2 更新条件

`CheckConditions(...)` 要求 running 类状态：

- `STATE_RUNNING`
- `STATE_RPA_MOVING_RUNNING`
- `STATE_MANEUVERING_RUNNING`

不满足时直接返回，不 reset。

### 7.4.3 核心逻辑

`AccEstimator` 使用 `Differentiator` 对车速绝对值做滤波微分：

```text
curr_speed = abs(vehicle_state.linear_velocity())
acc_estimated = differentiator.Update(curr_speed)
speed_estimated = differentiator.GetValue()
```

第一次运行时初始化 differentiator：

```cpp
Initialize(5.0, 0.1, 5.0, 0.1, curr_speed)
```

### 7.4.4 Controller 使用点

- `ConvertToTorque(...) -> LoadTorqueControllerInput(...)`：`input.acc_estimated_ = observer_->Get<double>(acc_estimator, "acc_estimated")`，用于`TorqueController::ComputeTorqueInStereoLot(...)`。机械库位里面地形复杂，而且平面不平，直接用 IMU acceleration，会非常抖，所以扭矩控制使用 `acc_estimated_` 作为加速度反馈，相对平滑，但有一定滞后性

## 7.5 `StereoObserver`
### 7.5.1 输出字段

`fields_map_`：

- `is_in_stereo_slope`
- `is_stereo_with_slope`
- `apply_stereo_control_cmd`
- `front_wheel_exit_slope_position`
- `stereo_stage`

### 7.5.2 更新条件

`CheckConditions(...)` 要求 running 类状态：

- `STATE_RUNNING`
- `STATE_RPA_MOVING_RUNNING`
- `STATE_MANEUVERING_RUNNING`

不满足时直接返回，不 reset。

`Update(...)` 执行三步：

```text
ObserveStereoLotRamp(observer_input)
UpdateStereoStage(observer_input)
apply_stereo_control_cmd_ = CheckStereoLotCondition(observer_input)
```

### 7.5.3 核心逻辑

#### 7.5.3.1 `CheckStereoLotCondition`

该函数决定是否启用机械库位特殊控制命令，即输出字段 `apply_stereo_control_cmd`。

机械库位由于有坡，所以需要一套特殊的后轮上坡预先加扭-库内保持匀速-前轮上坡预先加扭的逻辑，否则会溜坡，无法顺利进入库位。但是过程中需要考虑碰撞风险，所以由于如下判断

必须满足：

- `is_enter_stereo_lot_` 为 true。
- 碰撞决策不能是普通障碍停止类：
  - 如果是 `COLLISION_LAST_SEG_STEREO_OBSTACLE_STOP`，表示当前库位有工字钢，车辆需要在工字钢附近停车，确认安全再继续，何时退出机械库位逻辑，进行正常刹车需要根据与工字钢的相对位置、pitch 和速度来判断。此时后轮刚上坡不久，如果刹车过早，后轮可能上不了坡，太晚会导致在工字钢附近急刹
  - 如果 collision type 小于 `COLLISION_PARKING_SPACE_END_LINE_STOP`，说明有碰撞风险，返回 false。
- 当前 segment 必须是最后一个 segment。
- 不能处于“入口线附近且终点误差小”的场景： `distance_car_tail_to_entrance_line_ > -0.1`且 `abs(epoint.end_y_error) < 0.5`，这种情况表示当前轨迹只是在机械库位外挪库，不是要进入机械库位
- 当前档位不能是 D 档。

满足后返回 true。

#### 7.5.3.2 `ObserveStereoLotRamp`

目的：在后轮入库的过程中通过观测自身状态来估计得到机械库位入库坡度，以及入坡出坡的相对位置

先用 pitch differentiator 得到 `pitch_rate_`。车速超过阈值时计算得到入库坡度：

```text
slope_degree = asin(pitch_rate / linear_velocity)
```

再根据车尾到入口线的距离，识别坡道进入和退出位置：

- 超出观察起点时，重置进入/退出位置。
- 在观察范围内：
  - 如果尚未进入坡道，且 `slope_degree` 超过阈值，记录 `enter_slope_position_`。
  - 如果已进入但未退出，且 `slope_degree` 回落到阈值以下，并且距离变化超过阈值，记录 `exit_slope_position_`。

#### 7.5.3.3 `UpdateStereoStage`

目的：这是利用`ObserveStereoLotRamp`中得到的后轮入坡出坡的位置，通过轴距简单计算，可以得到前轮入坡出坡的位置，就可以将整个机械库位划分为如下stage，使得能够在机械库位内进行更为精细的控制

- `OUTSIDE`
- `REAR_WHEEL_CLIMBING`
- `REAR_WHEEL_INSIDE`
- `FRONT_WHEEL_CLIMBING`
- `INSIDE`

如果未进入机械库位，直接保持 `OUTSIDE`。

没有识别到坡道进入位置时，主要用车尾到入口线距离与车辆后悬、轴距判断：

- 车尾进入超过后悬距离：`REAR_WHEEL_INSIDE`
- 继续进入超过后悬 + 轴距：`INSIDE`

识别到坡道但还没识别到退出位置时：

- pitch 小于配置阈值并累计超过计数阈值，认为 `REAR_WHEEL_CLIMBING`。
- 同时仍会根据距离切到 `REAR_WHEEL_INSIDE` 或 `INSIDE`。

识别到完整坡道后：

- 根据后轮坡道进入/退出位置，加上轴距和前轮 offset，推算：
  - `front_wheel_enter_slope_position_`
  - `front_wheel_exit_slope_position_`
- 然后按当前 `distance_car_tail_to_entrance_line_` 判断：
  - 后轮在平台、前轮还在路面：`REAR_WHEEL_INSIDE`
  - 前轮爬坡区间：`FRONT_WHEEL_CLIMBING`
  - 前轮退出坡道后：`INSIDE`

如果 stage 为 `FRONT_WHEEL_CLIMBING` 或 `REAR_WHEEL_CLIMBING`，设置：

```cpp
is_in_stereo_slope_ = true;
```

### 7.5.4 Controller 使用点

机械库位完整逻辑查看Controller逻辑梳理中7.2节

