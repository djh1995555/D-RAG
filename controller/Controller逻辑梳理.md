梳理控制器模块结构。重点关注 app 入口 `parking_controller_processing_app` 以及主要泊车控制器 `parking_controller_new`

# 1. 模块总览

当前目录按职责大致分为以下几层：

```text
controller/
├── BUILD                         # 顶层 Bazel target 与配置打包
├── README.md                     # 离线编译运行说明
├── app/                          # 进程入口、App 生命周期、Proto 与内部数据转换
├── conf/                         # ap_control_cmd.pb.conf 等平台配置
├── proto/                        # 控制器本地 proto 配置
└── core/
    ├── data/                     # 控制器内部数据模型与 DataManager
    ├── motion/                   # APA/HPP/DOP motion 与状态机
    ├── control/                  # 具体控制器实现
    └── data_observer/            # 调试/观测辅助数据
```

核心链路可以理解为：

```text
node_launch_main
  -> ControlProcessingApp::InitApp()
  -> ControlProcessingApp::ProcessFrame()
  -> DataConvert 更新 DataManager
  -> APAMotion/HPPMotion::ProcessData()
  -> APA/HPP 状态机选择状态
  -> ParkingControllerNew::Handle* / ExecuteSegment()
  -> ControlProcessingApp::OnPublishData()
  -> DataConvert 输出 Proto
```

# 2. Controller选择

`core/motion/apa_motion.cc` 中，`APAMotion::Init()` 决定泊车控制器实现（`HPPMotion`同理）：

```cpp
if (enable_acc_interface()) {
  parking_controller_ = std::make_shared<ParkingController>(this);
} else {
  if (apa_controller_cloud_switch_) {
    parking_controller_ = std::make_shared<ParkingControllerNew>(this);
  } else {
    parking_controller_ = std::make_shared<ParkingControllerTorque>(this);
  }
}
```

因此在当前主链路下，`ParkingControllerNew` 是 APA motion 使用的主要 controller，但前提是：

- `enable_acc_interface()` 为 false。
- `apa_controller_cloud_switch_` 为 true，该标志位是对应的云控开关，表示可以通过云控开关对每个车型选择是采用`ParkingControllerTorque`还是`ParkingControllerNew`

# 3. `ParkingControllerNew` 结构

主要文件：

- `core/control/parking_controller_new.h`
- `core/control/parking_controller_new.cc`
- `core/control/parking_controller_new_partial_functions.cc`：由于`core/control/parking_controller_new.cc`单一文件体积过大拆分出来的附属文件

`ParkingControllerNew` 继承 `ParkingController`，重写大量 `Handle*Data()`、段执行、初始化和状态查询接口。

## 3.1 Init 分级方案

`ParkingControllerNew` 的 reset 不是单一“大清空”，而是按控制生命周期分层：

| 层级    | 函数                                 | 典型触发                   | 实用理解               |
| ----- | ---------------------------------- | ---------------------- | ------------------ |
| 任务级   | `ResetControlParamsByParking`      | READY 完整初始化            | 清“这次泊车任务”的东西       |
| 轨迹级   | `ResetControlParamsByTrjectory`    | 新轨迹、轨迹初始化              | 清“这条轨迹”的东西         |
| 状态切换级 | `ResetControlParamsSwitchingState` | `IsApaStateChanged()`  | 清“上一个 APA 状态遗留”的东西 |
| 段级    | `ResetControlParamsBySegment`      | segment init、轨迹级、状态切换级 | 清“当前轨迹段执行”的东西      |

**主要调用链**：

```text
HandleReadyData
  -> InitControlParameters
     -> ResetControlParamsByParking
     -> ResetControlParamsByTrjectory
        -> ResetControlParamsBySegment
     -> ResetControlParamsSwitchingState, only if IsApaStateChanged()
        -> ResetControlParamsBySegment

各 Handle*Data
  -> if IsApaStateChanged()
       ResetControlParamsSwitchingState
         -> ResetControlParamsBySegment

ApaTrajectoryInit
  -> ResetControlParamsByTrjectory
     -> ResetControlParamsBySegment

ApaExecuteStateInit
  -> ResetControlParamsBySegment
```

## 3.2 状态机 Handle 接口

`ParkingControllerNew` 中有两个 command 复用函数：

- `UnControlledCommand`
- `StaticControlCommand`

以及三个基础命令拼装函数：

- `SetLatCommand`
- `SetLonCommand`
- `SetGearCommand`

关系：

```cpp
UnControlledCommand
  -> Clear ControlOutput
  -> SetLonCommand(-0.017)
  -> 用底盘当前扭矩覆盖 target_torque_vcu/bcs
  -> SetLatCommand(current steer)
  -> SetGearCommand(default)
  -> PublishData
```

```cpp
StaticControlCommand
  -> Clear ControlOutput
  -> SetLatCommand(previous_target_steer)
  -> SetLonCommand(normal_stop_acc)
  -> SetGearCommand(default)
  -> PublishData
```

多数 `Handle*Data` 不是直接手写所有字段，而是按固定模式组合：

```cpp
observer_->Update(...)
controller_working_status_ = ...
if (IsApaStateChanged()) {
  ResetControlParamsSwitchingState(data_manager);
}
UpdateInfo(data_manager);

control_output_.Clear();
control_output_.cmd_type_ = CMD_TYPE_PARKING;
SetLatCommand(...);
SetLonCommand(...);
SetGearCommand(...);
PublishData(...);
```

这套设计把“怎么写控制字段”集中到 `SetLat/Lon/Gear`，各状态只决定目标值和是否允许 P 档/急刹。

车辆控制最核心的状态机是`RunningState`，对应的 `Handle*Data` 为`ExecuteSegment`

# 4. `ExecuteSegment`

`ExecuteSegment(...)` 是 `ParkingControllerNew` 的核心轨迹执行函数。输入包括：

- 当前 `DataManager`
- 当前 segment id
- 当前 `TrajectorySegment`
- 当前 `CollisionDecision`
- velocity planner 的 driving stage
- all task complete 标志

主流程：

```
1. 匹配当前车辆位置到轨迹点。
2. 更新 `apa_execute_state_`：
   - 当前 segment
   - point id
   - execution point error
   - collision decision
   - 当前剩余距离
1. 更新车位类型、机械库位进入距离、后视镜折叠请求等上下文。
2. 更新 observer
3. 根据 collision decision 或 observer 结果调整 segment stage
4. 按 `apa_execute_state_.segment_stage_` 进行 stage switch，执行不同状态下的操作
5. 状态机请求异常退出流程
6. 如果驾驶员踩刹车，强制 standstill
7. 调用 `ConvertToTorque(...)`
8. 调用 `PublishData(...)`
```

**核心控制过程都在stage switch 部分**

`ExecuteSegment(...)` 进入 stage switch 前，已经完成当前 segment、执行点、车辆状态、碰撞决策、observer 等上下文更新，这里简述以下最核心的`SEGMENT_STARTUP`、`SEGMENT_TRACKING`、`SEGMENT_STOPPING`的主要逻辑

三个 stage 的入口逻辑：

```text
SEGMENT_STARTUP
  -> setStatus(STATUS_STARTUP)
  -> ApaExecuteStartupStage(...)

SEGMENT_TRACKING
  -> setStatus(STATUS_TRACKING)
  -> ApaExecuteTrackingStage(...)

SEGMENT_STOPPING
  -> setStatus(STATUS_STOPPING)
  -> ApaExecuteStoppingStage(...)
  -> 判断是否可以无停换挡
```

## 4.1  `SEGMENT_STARTUP`

主要执行接口为`ApaExecuteStartupStage`

目的：

- 管理起步阶段的状态转移。
- 判断是否应该直接停车、进入 tracking，或继续 startup。

简单逻辑：

```
1. 默认 current = SEGMENT_STARTUP
2. 初始化部分起步/停车相关状态
3. 如果车辆已经接近终点且姿态误差满足，直接执行停车控制
4. 否则调用 ArrivingEndPoint 判断是否已到达停车区域
5. 否则调用 ApaExecuteNewStartup 执行起步控制
6. 起步完成则转 SEGMENT_TRACKING
7. 起步未完成则保持 SEGMENT_STARTUP
```

状态转移：

```text
接近终点 / ArrivingEndPoint 为 true
  -> ApaExecuteNewStopping(...)
  -> SEGMENT_STOPPING

ApaExecuteNewStartup(...) 返回 true
  -> SEGMENT_TRACKING

其他
  -> SEGMENT_STARTUP
```

**核心控制**：`ApaExecuteNewStartup`

目的：

- 生成起步阶段的控制输出。
- 判断起步是否完成。

简单逻辑：

```text
1. 重置部分起步相关状态和速度 PID
2. 如果还不能 drive-off，先调用 ApaExecuteNewStandStillSteering(...) 原地转向
3. 原地转向完成后，调用 ComputeControls(...) 计算基础加速度和转角
4. 根据终点距离、障碍、短 segment、低速 segment、speed bump 修正起步加速度
5. 调用 CalculateStereoAcc(...) 修正机械库位场景下的加速度，非机械库位忽略即可
6. 调用 LimiterControlSteer(...) 限制目标转角变化
7. 写入起步控制输出
8. 调用 FinishStartup(...) 判断是否进入 tracking
```

## 4.2  `SEGMENT_TRACKING`

主要执行接口为`ApaExecuteTrackingStage`

目的：

- 管理 tracking 阶段的控制路径和状态转移。

简单逻辑：

```text
1. 默认 current = SEGMENT_TRACKING
2. 调用 ApaObstacleCheckCondition(...) 判断是否走障碍 tracking
3. 障碍场景调用 ApaExecuteObstacleTracking(...)
4. 普通场景调用 ApaExecuteTracking(...)
5. 调用 StopEmergencyIfExceedEndPoint(...) 判断是否需要停车
6. 判断是否接近终点停车阈值
7. 调用 ArrivingEndPoint(...) 做动态终点判断
8. 如果 stuck_monitor 判断卡滞，则转 FINISHED
9. 更新异常标志并返回 current
```

状态转移：

```text
StopEmergencyIfExceedEndPoint(...) 为 true
  -> SEGMENT_STOPPING

接近终点阈值 / ArrivingEndPoint(...) 为 true
  -> SEGMENT_STOPPING

stuck_monitor.is_stuck 为 true
  -> SEGMENT_FINISHED

其他
  -> SEGMENT_TRACKING
```

**核心控制**： `ApaExecuteTracking`

目的：

- 普通 tracking 场景下生成控制输出。

简单逻辑：

```text
1. 调用 ComputeControls(...) 计算基础加速度和转角
2. 对小加速度做死区补偿
3. 根据 gear 转成车辆执行方向
4. 根据上一参考加速度和速度误差限制加速度
5. 大扭矩 overstop 时降低目标加速度
6. 调用 CalculateStereoAcc(...) 做机械库位修正
7. 调用 LimiterControlAcc(...) 做 jerk 限幅
8. 调用 LimiterControlSteer(...) 做转角限幅
9. 写入 tracking 控制输出
```

**核心控制**：`ApaExecuteObstacleTracking`

目的：

- 障碍场景下生成更偏制动和舒适减速的 tracking 输出。

简单逻辑：

```text
1. 调用 ComputeControls(...) 计算基础控制量
2. 根据当前速度、规划加速度、主缸压力生成 command_acc
3. 低速时使用舒适制动策略
4. 高速或已有压力时使用更明确的制动策略
5. 限制 command_acc 不超过正常停车下限
6. 大扭矩 overstop 时进一步限制加速度
7. 调用 CalculateStereoAcc(...) 做机械库位修正
8. 调用 LimiterControlAcc(...) 做 jerk 限幅
9. 调用 LimiterControlSteer(...) 做转角限幅
10. 写入控制输出
```

## 4.3  `SEGMENT_STOPPING`

主要执行接口为`ApaExecuteStoppingStage`

目的：

- 管理停车阶段控制和状态转移。

简单逻辑：

```text
1. 默认 current = SEGMENT_STOPPING
2. 调用 ApaExecuteNewStopping(...) 生成停车控制
3. 判断终点误差是否发生跳变，必要时准备回到 tracking
4. 调用 StopEmergencyIfExceedEndPoint(...) 继续做终点安全保护
5. 如果需要跳回 tracking，则调用 ApaExecuteTracking(...) 覆盖本周期输出
6. 如果车辆完全停止，则调用 ApaExecuteFinished(...)
7. 返回 current
```

状态转移：

```text
StopEmergencyIfExceedEndPoint(...) 为 true
  -> SEGMENT_STOPPING

终点误差跳变，需要重新跟踪
  -> SEGMENT_TRACKING

IsFullyStopped(...) 为 true
  -> SEGMENT_FINISHED

其他
  -> SEGMENT_STOPPING
```

**核心控制**：`ApaExecuteNewStopping`

目的：

- 生成停车阶段的目标加速度、目标转角和 standstill 请求。

简单逻辑：

```text
1. 调用 ComputeControls(...) 获取目标转角
2. 根据当前速度和剩余终点距离计算停车制动需求
3. 根据坡度修正最终制动强度
4. 调用 ComputeDecelerationJerk(...) 计算停车 jerk
5. 根据短 segment、超规划速度、大扭矩等情况修正 jerk
6. 如果纵向距离跳变且制动不足，则强制给更强制动
7. 否则调用 LimiterControlAcc(...) 平滑加速度
8. 调用 CalculateStereoAcc(..., true) 做机械库位停车修正
9. 调用 LimiterControlSteer(...) 限制转角
10. 写入停车控制输出
11. 调用 UpdateStandstillCommand(...) 更新静止保持请求
```

## 4.4 关键接口

### 4.4.1 `ArrivingEndPoint`

目的：

- 判断车辆是否已经进入终点停车区域。
- startup 和 tracking 都会使用它。

简单逻辑：

```text
1. 检查 end_y_error 是否发生明显跳变
2. 调用 PredictDisThreshold(...) 预测当前速度下应提前多少距离停车
3. 根据车速、规划速度、segment 长度、短 segment 状态修正停车阈值
4. 检查终点纵向误差、横向误差、航向误差是否满足停车条件
5. 返回 true/false
```

关键影响：

- 返回 true 时，当前 stage 会转入 `SEGMENT_STOPPING`。
- 如果检测到纵向距离跳变，会置位 `is_large_longitudinal_distance_jump_`，后续停车控制会更保守。

### 4.4.2 `StopEmergencyIfExceedEndPoint`

目的：

- 防止车辆超过终点或在终点附近制动距离不足。

简单逻辑：

```text
1. 计算当前相对终点的纵向距离
2. 根据速度和剩余距离估算需要的制动加速度
3. 判断主缸压力是否已经有效建立
4. 如果安全距离不足或已明显越过终点，则改写目标加速度
5. 高风险时请求 emergency brake，并更新 torque_controller 状态
6. 返回是否需要停车
```

调用位置：

```text
ApaExecuteTrackingStage(...)
ApaExecuteStoppingStage(...)
```

# 5. 扭矩转换与安全控制

## 5.1 总体调用位置

`ConvertToTorque(...)` 是 `ParkingControllerNew` 内部把“加速度/驻车/起步/停车等控制意图”转换成 VCU/BCS 扭矩请求的关键边界。

典型调用链：

```text
APA state / segment stage
  -> 构造 ControlOutput
     - req_target_acc_mpss
     - req_drive_off
     - req_stand_still
     - req_emergency_brake
     - steering / gear / EPB / AVH
  -> ConvertToTorque(data_manager, control_output)
  -> TorqueController::ComputeTorque(...)
  -> PublishData(...)
```

它主要在两类地方被调用：

- `SetLonCommand(...)`：多数状态级 `Handle*Data()` 会经由这里设置纵向命令并转扭矩。
- `ExecuteSegment(...)`：RUNNING 状态执行 segment stage 后，统一调用一次 `ConvertToTorque(...)`。

## 5.2 `ConvertToTorque` 主流程

函数签名：

```cpp
void ParkingControllerNew::ConvertToTorque(
    const DataManager& data_manager,
    ControlOutput& control_output,
    bool release_bcs_torque_flag = false)
```

主流程如下：

```text
  -> BoundControlCmd
  -> 更新previous_target_acc_mpss_
  -> set各种torque controller需要的标志位
  -> LoadTorqueControllerInput
  -> APA 进入 running 时 reset torque
  -> TorqueController::ComputeTorque
```

## 5.3 `TorqueController::ComputeTorque`

`ComputeTorque(data_manager, target_acc, control_output)` 负责生成：

- `control_output.target_torque_vcu`
- `control_output.target_torque_bcs`

内部可分为四层：

1. 判断方向。
2. 根据状态计算“总目标轮端扭矩”。
3. 将总目标扭矩分配到 VCU 和 BCS。
4. 做梯度限制并写 debug。

## 5.4 总目标扭矩计算分支

计算目标扭矩分为三个层级：分别为`standstill`，`creep`和`status_control`，`status_control`中也会区分是常规库位还是机械库位

优先级：

```text
keep_standstill_ -> ComputeTorqueStandstill
else is_creep_   -> ComputeTorqueCreep
else status_     -> 按状态分支计算
```

### 5.4.1 standstill

`TorqueController` 内部有 `keep_standstill_`：

- 如果当前还没 keep standstill，且 `req_standstill_` 为 true，则进入保持静止。
- 如果已经 keep standstill，且本帧有 `drive_off_flag_`，则退出保持静止。

这意味着只要进入了 keep standstill，普通 STARTUP/TRACKING/STOPPING 分支会被暂时绕过，直到 drive off。

`ComputeTorqueStandstill()`：

1. 计算坡道静止所需扭矩 `torque_for_standstill`。
2. 计算目标加速度对应 feedforward 扭矩。
3. 重置反馈项。
4. 取 `min(torque_feedforward_, torque_for_standstill)`。
5. 如果是机械库位且车尾距离入口线小于 `-3.5`，扭矩放大 2 倍（针对机械库位前轮在入库线附近的溜车的情况）

`ComputeStandstillTorque()` 中实际会调用 `VehicleModel::ComputeStandstillTorque(...)`，会计算当前的坡道分力，然后再乘 `1.5`（避免测量误差导致的制动力不足），并写入 debug 的 `raw_torque_for_standstill_`。

### 5.4.2 creep

专门针对短轨迹场景，具体逻辑可以查看7.5节

### 5.4.3 `ComputeTorqueInStereoLot`

专门针对机械库位，具体逻辑可以查看7.2节

### 5.4.4 常规计算目标扭矩

不同状态的流程基本一致

```
- 动力学模型计算扭矩前馈
- 加载对应控制参数
- 根据`target_acc - imu_acc * direction_`计算加速度误差
- 根据加速度误差计算扭矩反馈
- 对反馈进行滤波
- 返回前馈反馈之和作为目标扭矩
```

**注意点**：

`ComputeTorqueStartup`中为了让车辆更快起步，做了如下处理

```cpp
if (std::fabs(speed) < cross_zero_speed_threshold_) {
	acc_error_ = std::max(target_acc, 0.0);
} else {
	acc_error_ = target_acc - acc * direction_;
}
```

`ComputeTorqueStopping`中为了优化体感，做了如下处理，当速度小于 `0.15 m/s`，加速度误差置 0，避免低速停稳附近 PID 继续积分。

```cpp
if (std::fabs(speed) < 0.15) {
	acc_error_ = 0.0;
} else {
	acc_error_ = target_acc - acc * direction_;
}
```

## 5.5 VCU/BCS 扭矩分配

`ComputeTorque()` 得到总目标轮端扭矩 `target_torque` 后，会拆成：

- `target_torque_vcu`
- `target_torque_bcs`

### 5.5.1 `release_bcs_flag_`

`release_bcs_flag_` 来自外部，用于在泊车结束后，EPB和P档就位后，主动释放bcs扭矩。如果 `release_bcs_flag_` 为 true：

- VCU 维持上一帧：`target_torque_vcu = pre_target_torque_vcu_`
- BCS 释放到 0：`target_torque_bcs = 0`
- VCU 梯度固定 2000
- BCS 梯度由 `GetGradient(0, pre_target_torque_bcs_)` 计算

### 5.5.2 正扭矩

当 `target_torque > 0`：

- 坡度/横滚角较大时：
  - VCU 给目标正扭矩。
  - BCS 暂时保持上一帧。
  - 如果实际 wheel torque/target_torque 已经达到一定比例，则释放 BCS 到 0
  - **这个比例取决与pitch和roll角中较大的一个**

- 坡度/横滚角较小时：
  - BCS 直接为 0。
  - VCU 取 `target_torque + pre_target_torque_bcs_`来做一个平滑的衔接

BCS 梯度通常由 `GetGradient(...)` 根据目标 BCS 扭矩变化量查表插值得到。

这段逻辑的意图是起步/驱动时协调电机扭矩建立与制动释放，尤其在坡上避免过早释放导致溜车。

### 5.5.3 负扭矩

当 `target_torque <= 0`：

- 坡度/横滚角较大：
  - 类似正扭矩的处理，来防止在爬坡到达轨迹终点时，在bcs尚未建压时卸掉vcu扭矩导致溜车
- 否则：
  - VCU 为 0。
  - BCS 给目标负扭矩。

BCS 梯度通常由 `GetGradient(...)` 根据目标 BCS 扭矩变化量查表插值得到。

如果 `keep_standstill_` 且从较大正 VCU 扭矩切到较大负 BCS 扭矩，并且坡向与档位满足特定条件，会把 BCS 梯度减半，降低车身抖动异响

```cpp
double vcu_bcs_torque_delta = pre_target_torque_vcu_ - target_torque_bcs;
if (keep_standstill_ && vcu_bcs_torque_delta > 1000 && pre_target_torque_vcu_ > 500 &&
((data_manager.vehicle_state().pitch_rad() < 0 && data_manager.vehicle_state().gear == VehicleStateGear::GEAR_POSITION_REVERSE) ||
(data_manager.vehicle_state().pitch_rad() > 0 && data_manager.vehicle_state().gear == VehicleStateGear::GEAR_POSITION_DRIVE))){
	target_gradient_bcs *= 0.5;
}

```

## 5.6 注意点

### 5.6.1 方向 direction_

根据当前档位设置：

- D 档：`direction_ = 1`
- R 档：`direction_ = -1`
- 其他：`direction_ = 0`

还有一个特殊的 `is_reverse_drag` 判断：

- R 档但车速为正，且目标加速度为负。
- D 档但车速为负，且目标加速度为负。

这代表当前处在“反向拖拽/反向制动”场景，代码会把 `direction_` 取反，使反馈误差方向与实际运动方向匹配。

### 5.6.2 PID 反馈重置条件

在一些状态切换或积分项风险场景下会调用 `ResetFeedbackPart()`：

- 非 STARTUP 切到 STARTUP。
- STOPPING 切到 TRACKING。
- 低速下目标加速度为正，但 PID 积分项过负。
- DRAG_TORQUE 切到 REVERSE_STARTUP。
- 机械库位需要制动但积分项为正。
- 上一帧 creep，本帧退出 creep。

`ResetFeedbackPart()` 会：

- 重置 PID。
- 清空 `torque_feedback_`。
- 重置反馈扭矩低通滤波器。

### 5.6.3 `is_crossing_over_`

针对减速带或者库位口路沿等场景设置的标志位，当接受到该标志位，需要将扭矩快速卸掉，主要做了以下操作

- 期望扭矩截到0以下
- 重置反馈项
- 设置大斜率

### 5.6.4 `is_sliping_`

针对溜车情况设置的标志位，当接受到该标志位，需要将快速建立大刹车扭矩（-8000，斜率20000）

## 5.7 关键状态对输出的影响总结

| 条件/状态 | 影响 |
| --- | --- |
| `req_stand_still` | 进入 `keep_standstill_`，优先使用 standstill 扭矩 |
| `req_drive_off` | 退出 `keep_standstill_` |
| `is_creep_` | 使用 creep 扭矩分支 |
| `is_stereo_lot_` | 多数分支改用机械库位 PID 与 `acc_estimated_` |
| `is_crossing_over_` | 目标扭矩不允许为正，梯度加大 |
| `is_sliping_` | 目标扭矩强制 `-8000`，梯度加大 |
| `release_bcs_flag_` | BCS 目标释放到 0，VCU 维持上一帧 |

# 6. Observer逻辑梳理

具体内容查看[[Obersver逻辑梳理]]

# 7. 细节功能梳理

## 7.1 档位接管

目的：主要逻辑是新增 `STATE_PARKING_TAKEOVER` 状态机处理档位接管逻辑

`DataManager` 中的 `APAState` 新增：

```text
STATE_PARKING_TAKEOVER = 35
```

`ControllerWorkingStatus` 新增：

```text
FinishParkingTakeover = 35
```

### 7.1.1 档位信号转换

`core/data/vehicle_state.h` 新增 `DriveTargetGear`，用于承接外部状态机输入的驾驶员目标挡位，但是由于MCU状态机定义与控制内部不同，需要进行转换

```cpp
enum class DriveTargetGear {
  GEAR_POSITION_UNSPECIFIED = 0,
  GEAR_POSITION_PARKING = 1,
  GEAR_POSITION_REVERSE = 2,
  GEAR_POSITION_NEUTRAL = 3,
  GEAR_POSITION_DRIVE = 4,
};
```

`core/data/parking_state_machine.h` 中通过 `set_parking_req_driver_target_gear(...)` 将该输入转换为控制内部使用的 `VehicleStateGear`：

| 外部输入 `DriveTargetGear` | 内部保存 `VehicleStateGear` |
| --- | --- |
| `GEAR_POSITION_PARKING` | `GEAR_POSITION_PARKING` |
| `GEAR_POSITION_REVERSE` | `GEAR_POSITION_REVERSE` |
| `GEAR_POSITION_NEUTRAL` | `GEAR_POSITION_NEUTRAL` |
| `GEAR_POSITION_DRIVE` | `GEAR_POSITION_DRIVE` |
| `UNSPECIFIED` / default | `GEAR_POSITION_UNSPECIFIED` |

这个字段最终通过 `parking_req_driver_target_gear()` 给 controller 读取。

### 7.1.2 触发条件

核心接口是 `DataManager::IsParkingTakeover()`：

```cpp
return ((apa_rpa_status == TERMINATED || hpp_status == TERMINATED) &&
        parking_brake_status == PARKINGTAKEOVER);
```

最终含义：

1. APA/RPA 或 HPP 外部状态机已经进入 `TERMINATED`。
2. `parking_brake_status` 明确是 `PARKINGTAKEOVER`。
3. 两者同时满足，控制侧认为当前不是普通异常退出，而是用户通过换挡触发的泊车接管。

该判断被多个 APA state 统一使用，用来跳转到 `STATE_PARKING_TAKEOVER`。

### 7.1.3 `HandleParkingTakeoverData`

主要逻辑：

```text
1. 更新 observer 和控制器状态
2. 状态切换时 reset 控制参数
3. UpdateInfo(data_manager)
4. 清除 control_output
5. 默认 command_acc = min(previous_target_acc_mpss_, -0.5)，表示换档成功之前都是处于刹车减速状态
6. 调用 ExcuteGearTakeover(data_manager)
7. 如果换挡接管已完成，将 command_acc 置 0，并设置工作状态 FinishParkingTakeover
8. 复用 SetLatCommand / SetLonCommand 输出横纵向控制
9. PublishData
```

行为含义：

- 未完成换挡接管前，控制器继续给停车制动。
- `ExcuteGearTakeover(...)` 判断驾驶员目标挡位是否已经满足。
- 满足后认为换挡接管完成，纵向加速度请求置 0，工作状态设为 `FinishParkingTakeover`。

### 7.1.4 `ExcuteGearTakeover`

如果外部输入不是 `UNSPECIFIED`，则更新 controller 内部缓存：

```cpp
if (parking_req_driver_target_gear() != GEAR_POSITION_UNSPECIFIED) {
  parking_req_driver_target_gear_ = parking_req_driver_target_gear();
}
```

这样做的效果：

- 外部目标挡位短暂有效时，controller 仍可保留最近一次明确的驾驶员意图。
- reset 控制参数时会把 `parking_req_driver_target_gear_` 清回 `UNSPECIFIED`。

满足车速和扭矩要求后，可以按照目标档位发送档位指令，直到实际档位与目标档位一致，同时还要松开epb。如果当前epb时拉起的，有没有松开，即使车辆挂到了目标档位，2秒后也会被VCU强制切换回P档

## 7.2 机械库位

机械库位和普通库位最大的不同就是有坡，而且库位深度较短，往往前轮刚上坡，后轮就要撞到限位杆，所以就需要在前轮上坡的时候的提前减速。减速的时机非常重要，需要根据车速和入库坡度来设计，过早前轮无法上坡，过晚会撞到限位杆

主要逻辑：

```text
1. observer 中的 stereo_observer，更新各种机械库位控制相关变量
2. ApaExecuteNewStartup，ApaExecuteSwitchWithoutStopStartup，ApaExecuteTracking，ApaExecuteObstacleTracking，ApaExecuteNewStopping中执行CalculateStereoAcc，利用stereo_observer的各种相关变量计算对应控制指令，会覆盖掉前面计算的纵向指令
3. stereo_observer的各种相关变量还传到torque_controller，进行特殊处理
```

关键变量：

```
is_target_slot_stereo_：表示是否为机械库位
distance_car_tail_to_entrance_line_：表示车尾到入库线的距离
```

### 7.2.1 `stereo_observer`

具体内容查看[[Obersver逻辑梳理]] 7.5节

使用字段包括：

| 字段 | 类型 | 作用 |
| --- | --- | --- |
| `apply_stereo_control_cmd` | `bool` | 是否启用机械库位控制修正 |
| `is_stereo_with_slope` | `bool` | 当前机械库位是否识别到完整坡道 |
| `front_wheel_exit_slope_position` | `double` | 前轮出坡位置 |
| `stereo_stage` | `StereoStage` | 当前车辆相对机械库位坡道的阶段 |
| `is_in_stereo_slope` | `bool` | 当前是否处于坡道阶段，主要给 jerk / torque / debug 使用 |

### 7.2.2 `CalculateStereoAcc`

`CalculateStereoAcc(double target_acc, bool is_stopping)` 用于在机械库位场景下修正纵向目标加速度。

普通泊车控制会先根据启动、跟踪、避障或停车逻辑算出一个基础 `target_acc`，然后在机械库位控制生效时调用 `CalculateStereoAcc(...)` 做二次修正。

核心目的：

1. 进入机械库位时适当补正加速度，帮助车辆爬坡。
2. 前轮爬坡阶段使用专门的爬坡加速度。
3. 接近坡道或车位终点时提前进入制动。
4. 根据有无坡道调整停车距离阈值。
5. 把机械库位的阶段信息继续传给 torque controller。

#### 7.2.2.1 判断是否启用机械库位控制

关键保护：

```cpp
if (!observer_->Get<bool>(Component::stereo_observer,
                          "apply_stereo_control_cmd")) {
  return target_acc;
}
```

如果 `StereoObserver` 没有允许机械库位控制，函数直接返回原始 `target_acc`。

因此，`CalculateStereoAcc(...)` 是非侵入式修正：普通车位、非最后段、D 挡、碰撞决策不匹配等场景不会被它改变。

#### 7.2.2.2 计算停止距离阈值

先根据是否识别到完整坡道选择 gain：

```cpp
slot_with_slope = observer_->Get<bool>("is_stereo_with_slope");
gain = slot_with_slope ? acc_gain_with_slope : acc_gain_without_slope;
```

然后估计制动距离：

```cpp
estimated_acc = gain * final_brake_acc;
distance_threshold = speed * speed / (2 * estimated_acc);
```

由于 `final_brake_acc` 是负值，因此 `distance_threshold` 是负距离。

随后按车型和坡道状态限幅：

```text
默认范围：[-2.0, -0.15]
MS11 / MS11_P 且有坡：[-0.5, -0.15]
MS11 / MS11_P 且无坡：[-2.0, -0.4]
```

最终写入：

```cpp
stop_distance_ = distance_threshold;
```

该阈值用于 stopping 阶段判断是否需要最终制动。

#### 7.2.2.3 计算剩余距离和前轮出坡距离

根据轨迹计算剩余距离：

```cpp
rest_distance =
    apa_execute_state_.epoint_.end_y_error * apa_execute_state_.segment_.gear;
```

但有时机械库位终点的终点并不合理，可以计算当前位置到前轮出坡位置的距离来得到一个更合理的剩余距离：

```cpp
distance_to_front_wheel_exit_slope_position_ =
    front_wheel_exit_slope_position - distance_car_tail_to_entrance_line_;
```

如果当前阶段是 `FRONT_WHEEL_CLIMBING`，并且终点和前轮出坡目标非常接近：

```cpp
if (error_of_two_targets < 0.25 && error_of_two_targets > 0.0) {
  rest_distance = distance_to_front_wheel_exit_slope_position_;
}
```

含义：

- 前轮爬坡时，如果“终点”和“前轮出坡点”只差一点，优先把前轮出坡点作为控制目标。
- 避免车辆在前轮尚未完全出坡时按终点刹停。

#### 7.2.2.4 need_brake_ 状态

只有 `is_stopping == true` 时会触发最终制动状态：

```cpp
if (is_stopping && !need_brake_ &&
    (rest_distance > stop_distance_ || stereo_stage == StereoStage::INSIDE)) {
  need_brake_ = true;
}
```

退出条件：

```cpp
else if (need_brake_ &&
         distance_car_tail_to_entrance_line_ > entrance_line) {
  need_brake_ = false;
}
```

含义：

- 停车阶段，如果剩余距离进入制动阈值，或已经进入 `INSIDE`，则开始最终制动。
- 如果车辆又回到入口线外侧，则清除制动状态。

#### 7.2.2.5 按 StereoStage 修正加速度

##### 7.2.2.5.1 OUTSIDE / REAR_WHEEL_CLIMBING

```cpp
if (distance_car_tail_to_entrance_line_ >= rear_wheel_finish_climbing_position &&
    speed < max_speed) {
  target_acc = std::max(entrance_slot_acc, target_acc);
}
```

作用：

- 车还在入口或后轮爬坡附近时，如果速度低于 `1.0m/s`，至少给到 `entrance_slot_acc`。
- 避免机械库位入口爬坡动力不足。

##### 7.2.2.5.2 REAR_WHEEL_INSIDE

只有 `is_stopping == true` 时特殊处理：

```text
need_brake_ == true      -> final_brake_acc - 0.001
speed < 0.7              -> max(0.051, target_acc)
speed > 1.0              -> min(-0.201, target_acc)
其他                     -> max(0.0, target_acc)，匀速
```

作用：

- 后轮进入平台后，如果还没到最终制动点，会根据速度给轻微驱动或轻微制动。
- 如果已经进入 `need_brake_`，则转为最终制动。

##### 7.2.2.5.3 FRONT_WHEEL_CLIMBING

```cpp
target_acc = front_wheel_climbing_acc;
if (is_stopping && need_brake_) {
  target_acc = final_brake_acc - 0.002;
}
```

作用：

- 前轮爬坡阶段强制使用前轮爬坡加速度。
- 如果 stopping 阶段已经需要刹停，则使用最终制动。

##### 7.2.2.5.4 INSIDE

```cpp
if (rest_distance > inside_stereo_slot_dist_threshold_) {
  target_acc = final_brake_acc - 0.003;
}
```

`inside_stereo_slot_dist_threshold_` 默认是 `-0.15`。

作用：

- 车辆已经进入机械库位内部，且剩余距离进入阈值后，给最终制动。


### 7.2.3 `TorqueController`部分

多个状态都会优先判断 `is_stereo_lot_`，成立则使用 `ComputeTorqueInStereoLot()`：

- 使用 `VehicleModel::ComputeTorque(..., pitch_gain_)`计算前馈扭矩，其中要注意pitch_gain_的含义，主要是针对`StereoStage::REAR_WHEEL_INSIDE`状态（来自于`stereo_observer`），因为此时车辆pitch不为0，但是实际上没有斜坡分力，需要将pitch_gain设置为0，不然在库位会误以为在爬坡，而输出大扭矩
- 加速度反馈使用 `input_.acc_estimated_`，而不是直接用 `imu_acc`，机械库位里面地形复杂，而且平面不平，直接用 IMU acceleration，会非常抖，所以扭矩控制使用 `acc_estimated_` 作为加速度反馈，相对平滑，但有一定滞后性
- 默认 PID 参数为 `PARAM_IDX_STEREO_LOT`。如果阶段是 `FRONT_WHEEL_CLIMBING`，改用 `PARAM_IDX_FRONT_WHEEL_CLIMBING_STEREO_LOT`，针对前轮爬坡场景专门调整参数
- STARTUP 且沿 segment 方向速度很小时，误差取 `max(target_acc, 0)`，直到起步，起步后采用正常误差，误差为 `target_acc - acc_estimated`。
- 计算反馈扭矩并返回整体扭矩

## 7.3 异常退出

这里的异常退出指的是状态机请求退出，主要逻辑参考`DataManager::ApaStateNormal()`或`DataManager::HppStateNormal()`

当信号`apa_rpa_status`或者`hpp_status`等于TERMINATED时，表示MCU端要求异常退出，但是还需要监控`parking_brake_status`的值

```
enum class ParkingBrakeStatus {
	NOREQUEST = 0,
	NOBRAKE,
	SLOWBRAKE,
	EMERGENCYBRAKE,
	PARKINGTAKEOVER,
};
```

在这里需要分多种情况

### 7.3.1 `parking_brake_status = EMERGENCYBRAKE`

表示需要立刻跳转到`AbnormalStoppingState`，然后开始急刹，挂档等一系列流程

### 7.3.2 `parking_brake_status = PARKINGTAKEOVER`

表示请求档位接管，和异常退出逻辑无关，具体逻辑查看7.1节

### 7.3.3 `parking_brake_status < EMERGENCYBRAKE`

这表示MCU状态机要求缓刹，具体刹车逻辑如下

```cpp
  if (apa_status == 8 || hpp_status == 7 || apa_status == 6 ||
      hpp_status == 5) {
    double control_acc = -1.0;
    double speed = std::fabs(vehicle_state_.linear_velocity());
    double distance = 0.0;
    if (std::fabs(vehicle_state_.linear_velocity()) <= 0.3) {
      control_acc = std::min(-0.4, control_output_.req_target_acc_mpss());
    } else {
      control_acc = std::min(-0.7, control_output_.req_target_acc_mpss());
    }
    if (control_output_.req_target_acc_mpss() >= -0.1) {
      distance = speed * 0.3 + speed * speed / (2 * std::fabs(control_acc));
    } else {
      distance = speed * speed / (2 * std::fabs(control_acc));
    }
    double rest_distance = apa_execute_state_.epoint_.end_y_error *
                           apa_execute_state_.segment_.gear;
    if (-distance > rest_distance) {
      LimiterControlAcc(&control_acc, 1.5, comfort_target_acc_mpss_);
      comfort_target_acc_mpss_ = control_acc;
    } else {
      comfort_target_acc_mpss_ = control_output_.req_target_acc_mpss();
    }
    control_output_.set_req_target_acc_mpss(control_acc);
    torque_controller_->setStatus(TorqueController::Status::STATUS_STOPPING);
  } else {
    comfort_target_acc_mpss_ = 0.0;
  }
```

当车辆静止时再跳转到`AbnormalStoppingState`

**注意点**

目前发现档位接管期间，有可能发生由于时序问题导致的`apa_rpa_status`（或者`hpp_status`）和`parking_brake_status`错位，即`apa_rpa_status`或者`hpp_status`等于TERMINATED时，`parking_brake_status`提前从4变成0，导致车辆误触发了异常退出流程，会挂P档，导致用户无法顺利完成档位接管。所以针对APA功能，专门把`apa_rpa_status等于TERMINATED + parking_brake_status等于NOREQUEST`这个组合去掉，不让他触发异常退出

## 7.4 点到点控制衔接

`UpdateStateOfSwitchingCruising(const DataManager& data_manager)` 用于在泊出接近结束时，判断是否需要请求点到点衔接，点到点功能包含APA衔接HPP和衔接CNOA

它本身不直接切状态机，而是满足条件后更新 controller 内部状态：

```cpp
apa_control_mode_request_cruising_
```

该字段随后通过 `ControlOutput` 输出给状态机 / HMI，用于表达“APA 控制模式请求切到 cruising”。

**调用顺序**：

```cpp
parking_controller->ExecuteSegment(...);
parking_controller->UpdateStateOfSwitchingCruising(data_manager);
parking_controller->set_switch_parking_has_velocity(false);
```

也就是说，在每个 running 周期中，先执行当前泊车 segment 控制，再刷新是否需要切换到 cruising。

**关键变量**

```
point_to_point_state：专门表示点到点功能的标志位
hpp_status
hpp_active_sub_status
apa_rpa_status
apa_rpa_active_sub_function_status
```

## 7.5 短轨迹控制

### 7.5.1 判断短轨迹

在`SEGMENT_SWITCH_GEAR`状态下可以直接判断是否为短轨迹
在`SEGMENT_SWITCH_GEAR_WITHOUT_STOP`状态下，表示当前处于不停车换档，需要考虑两种情况

- 重规划：直接判断是否为短轨迹
- 不重规划：需要判断下一段轨迹的长度，因为当前实际上还处于上一段轨迹的末端

**注意点**

有一种情况时，刚收到的时候是短轨迹，但是后来变长了，所以需要以下逻辑来实时更新标志位

```cpp
double end_y_error = -apa_execute_state_.epoint_.end_y_error * apa_execute_state_.segment_.gear;
if (is_execution_short_segment_) {
	is_execution_short_segment_ = (end_y_error < short_segment_length_threshold_);
}
```

### 7.5.2 蠕行控制

`is_creep_` 在 `ParkingControllerNew::ConvertToTorque(...)` 中计算：

```cpp
is_creep_ = (is_execution_short_segment_ &&
             !(is_target_slot_stereo_ && IsEnteringStereoSlot()) &&
             (control_output_.req_drive_off() ||
              torque_controller_->getStatus() ==
                  TorqueController::Status::STATUS_TRACKING) &&
             (data_manager.parking_state_machine().apa_rpa_status() ==
                  data::ApaRpaStateMachine::ACTIVE ||
              data_manager.parking_state_machine().hpp_status() ==
                  data::ParkingHppStateMachine::ACTIVE) &&
             !observer_->Get<bool>(Component::large_torque_monitor,
                                   "large_torque_overstop_flag") &&
             !observer_->Get<bool>(Component::large_torque_monitor,
                                   "overspeed_flag"));
```

然后会被传入到torque_controller里进行蠕行控制`ComputeTorqueCreep()`：

- 低速 `abs(speed) < cross_zero_speed_threshold_` 时：
  - 目标加速度设为 `0.1`
  - 计算 feedforward和feedback
  - creep 额外扭矩为 `150 + feedback`
- 否则：
  - 目标加速度设为 0
  - creep 额外扭矩为 0
- 返回 `feedforward + creep_torque`

该逻辑用于短 segment 慢速蠕行，避免普通跟踪控制在短距离里过于激进或停滞。

# 8. 常用脚本
## 8.1 报告生成脚本
## 8.1.1 前置操作

#### 8.1.1.1 编译解析record文件：

进入目录：
```
cd mipilot/modules/parking/controller
```

checkout 到分支：
```
sandbox/dongjianhao/parse_dev
```

编译：
```
./build.sh mipilot/modules/parking/controller:avp_control_debug
```

**后续如果有新加的debug信息，需要在debug_app.cc文件里更新解析代码，才能在生成的`json`文件中找到新增的debug信号**
### 8.1.2 脚本操作

`bash start_generate_report.sh record_dir`

执行该脚本会先调用`avp_control_debug`来将record解析成`json`文件，再用`report_generator/report_generator.py`来在`record_dir`目录下生成`html`文件

config文件可以用来指定`html`文件的布局，每个subpanel的标题，显示哪些信号等
```
Speed: {
	"vehicle_speed": "chassis:vehicle_speed",
	"planned_speed": "hpp_debug:v_planned",
},
StopDistance: {
	"end_y_error": "control_debug:end_y_error",
}
```

## 8.2 数据回灌脚本
### 8.2.1 前置操作

将以下配置文件里的 `ap_control_cmd` 和 `vehicle_info` 的相对路径改为绝对路径

```
./mipilot/conf/cross_platform/parking/controller/node_launch_controller_debug.pb.conf
```

注释掉:
```
input_channels{
	name : "/parking/avp/state_machine"
}
```

新增：
```
input_channels {
	name : "/parking/router/status"
}
```

代码修改：
```
ControlProcessingApp::CheckTimeValid中的valid都置为true，不然会直接因为时间戳不对，回灌失败
ControlProcessingApp::CheckObstacleMapTimeValid的valid都置为true，不然会直接因为时间戳不对，回灌失败
running_state.cc中的!parking_controller->GetMonitorSafetyFlag()注释掉，不然偶尔会影响回灌结果
```

**以上操作，可以通过执行脚本中的`replay_adaption_apply.sh`来完成，`replay_adaption_revert.sh`用于回撤修改**

编译 recorder

```
./build.sh mipilot/ados/tools/recorder:recorder
```

编译控制节点：

```
./build.sh mipilot/modules/parking/controller/...
```

编译 roudi：

```
bazel build --config gcc-x86_64 @iceoryx//iceoryx_posh:iox-roudi
```

运行 roudi：

```
bazel-bin/external/iceoryx/iceoryx_posh/iox-roudi -m on -d ./
```

### 8.2.2 手动回灌

- **运行节点**：

```
./bazel-bin/mipilot/modules/parking/controller/app/node_launch_controller \
  mipilot/conf/cross_platform/parking/controller/node_launch_controller_debug.pb.conf \
  2>&1 | tee file.txt
```

- **播放 record**：

```
recorder play -f record_filepath \
  -k /parking/controller/command \
     /parking/controller/debug \
     /parking/controller/hmi_report \
     /parking/controller/status \
```

后面-k表示屏蔽掉的 channel，这四个通道的数据会由控制节点再次输出，下面录到的就是新的数据

- **录包**：

```
recorder record -c /parking/controller/command \
  /parking/controller/debug \
  /parking/controller/hmi_report \
  /parking/controller/status \
  -o /home/mi/debug/scripts/record/replay_record/replay.record
```

- **生成报告**：参考8.1节
### 8.2.3 脚本回灌

采用以下指令进行回灌

```
bash start_replay.sh replay_dir record_dir 单目录回灌
bash start_replay.sh replay_list 多目录回灌，将需要回灌的目录写在record_dirs.lst里
```

回灌后，会在replay_record目录下生成以回灌时间为目录的文件夹

注意：
建议设置一个独立文件夹编译recorder，然后把路径加入`~/.bashrc`，这样有两个好处，可以不用每个`repo`都编译recorder，并且可以直接通过`recorder cmd`来执行对应指令，`record_replayer/record_replayer.py`脚本中也是这么写的，如果用的是当前`repo`的recorder，那脚本中需要修改`play_cmd`和`record_cmd`