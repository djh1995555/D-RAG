# RACK Tool 重构设计文档

**文档版本:** 1.4
**创建日期:** 2026-03-24
**更新日期:** 2026-03-24
**作者:** AI Agent
**状态:** 已批准

**修订记录:**
- v1.4: 新增开环控制使能开关 (enabled 字段)
- v1.3: 修复 OpenLoopPanel 缺少 [保存] 按钮的问题；修复章节编号
- v1.2: 新增屏幕自适应、参数持久化；修改提交模式为统一批量提交；新增 SubmitType 区分调参和开环控制
- v1.1: 修复 Spec Review 发现的问题（调参提交机制、ControllerSignal 结构、心跳机制）

---

## 1. 概述

### 1.1 背景

现有 `rack_tool` 是停车控制器的实时调试可视化工具，基于 ImGui + ImPlot 开发。主要功能包括：
- 实时曲线绘制
- 参数在线调节

现有架构存在以下问题：
1. 参数定义硬编码在 `ImGuiApp` 类中（约 80 个 `std::atomic<float>` 成员变量），维护困难
2. 缺少开环控制能力，无法进行车辆直接控制测试
3. UI 布局固定，无法灵活调整

### 1.2 目标

重构 `rack_tool`，实现：
1. **在线调参功能** - 重构现有调参能力，采用 Proto 反射 + UI 配置驱动
2. **开环控制功能** - 新增档位、横向（方向盘）、纵向（加速度/扭矩）控制能力
3. **可扩展监控** - 信号监控支持便捷扩展
4. **屏幕自适应** - 对不同尺寸的屏幕自适应调整 UI 大小
5. **参数持久化** - 支持保存当前参数，下次启动自动加载

### 1.3 约束

| 约束项 | 说明 |
|--------|------|
| 仓库关系 | `parking/controller`、`rack_tool`、Proto 定义分属三个独立仓库 |
| 部署方式 | `rack_tool` 需单独部署 |
| UI 框架 | 继续使用 ImGui + GLFW + OpenGL3 |
| 通信方式 | Iceoryx 进程间通信 |

---

## 2. 整体架构

### 2.1 架构图

```
┌──────────────────────────────────────────────────────────────────┐
│                        RackToolApp (主应用)                        │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                    ImGuiApp (DockSpace 框架)                 │  │
│  │  ┌─────────────────────────────────────────────────────┐   │  │
│  │  │              MonitorPanel (监控面板 - 上半部)         │   │  │
│  │  └─────────────────────────────────────────────────────┘   │  │
│  │  ┌─────────────────────────────────────────────────────┐   │  │
│  │  │  [调参面板] [开环控制] - Tab 切换                      │   │  │
│  │  ├─────────────────────────────────────────────────────┤   │  │
│  │  │  ParamsPanel / OpenLoopPanel (下半部)                │   │  │
│  │  └─────────────────────────────────────────────────────┘   │  │
│  └────────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                    DataLayer (数据层)                        │  │
│  │  ProtoReflectionEngine │ UIConfigLoader │ SafetyManager    │  │
│  └────────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                 IceoryxBridge (通信层)                       │  │
│  └────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

### 2.2 模块职责

| 模块 | 文件位置 | 职责 |
|------|----------|------|
| RackToolApp | `apps/rack_tool_app.h/cc` | 应用生命周期管理，继承 `ados::apprt::api::App` |
| ImGuiApp | `core/imgui_app.h/cc` | DockSpace 窗口管理，Tab 切换，屏幕自适应 |
| ParamsPanel | `panels/params_panel.h/cc` | 调参面板，Proto 反射 + UI 配置驱动 |
| OpenLoopPanel | `panels/open_loop_panel.h/cc` | 开环控制面板，档位/横向/纵向控制 |
| MonitorPanel | `panels/monitor_panel.h/cc` | 实时监控面板，子面板 + 曲线绘制 |
| ProtoReflectionEngine | `engine/proto_reflection_engine.h/cc` | Proto 字段遍历与值读写 |
| UIConfigLoader | `engine/ui_config_loader.h/cc` | 加载 UI 配置文件 (JSON) |
| SafetyManager | `engine/safety_manager.h/cc` | 心跳检测、限值钳位、急停处理 |
| ParamPersistence | `engine/param_persistence.h/cc` | 参数持久化，保存/加载到本地文件 |
| IceoryxBridge | `bridge/iceoryx_bridge.h/cc` | Iceoryx 通信封装 |

---

## 3. 目录结构

```
rack_tool/
├── apps/
│   ├── rack_tool_app.h/cc          # 主应用入口
│   └── launch_rack_tool_app.cc     # 程序 main
├── core/
│   ├── imgui_app.h/cc              # DockSpace 框架管理
│   └── data_layer.h/cc             # 数据层核心
├── panels/
│   ├── params_panel.h/cc           # 调参面板
│   ├── open_loop_panel.h/cc        # 开环控制面板
│   └── monitor_panel.h/cc          # 监控面板
├── engine/
│   ├── proto_reflection_engine.h/cc # Proto 反射引擎
│   ├── ui_config_loader.h/cc        # UI 配置加载器
│   ├── safety_manager.h/cc          # 安全管理器
│   └── param_persistence.h/cc       # 参数持久化
├── bridge/
│   └── iceoryx_bridge.h/cc          # Iceoryx 通信封装
├── config/
│   ├── params_ui_config.json        # 调参 UI 配置
│   └── monitor_config.json          # 监控信号配置
├── proto/
│   └── rack_tool.proto              # 扩展消息定义
├── conf/
│   └── rack_tool_app.pb.conf        # 应用配置
└── scripts/
    ├── rack_tool.sh                 # 启动脚本
    ├── build_rack_tool.sh           # 构建脚本
    └── build_rack_tool_tar.sh       # 打包脚本
```

---

## 4. 数据流设计

### 4.1 订阅通道

| 通道名 | Iceoryx Topic | Proto 类型 |
|--------|---------------|------------|
| PastParkingChassis | `/sensors/chassis/parking` | ParkingChassis |
| ParkingStateMachine | `/parking/apa/state_machine` | ParkingStateMachine |
| APControlCmd | `/parking/controller/command` | APControlCmd |
| APControlDebug | `/parking/controller/debug` | APControlDebug |
| ParkingControllerToStateMachine | `/parking/controller/status` | ParkingControllerToStateMachine |
| APControlToHMI | `/parking/controller/hmi_report` | APControlToHMI |

### 4.2 发布通道

| 通道名 | Iceoryx Topic | Proto 类型 |
|--------|---------------|------------|
| ControllerSignal | `/manual/controller/signal` | ControllerSignal |

> 调参信号和开环指令共用同一个发布通道。

### 4.3 数据流向

```
订阅数据 → ProtoReflectionEngine 解析 → DataContainer 存储
                                              ↓
UIConfigLoader 加载配置 → 渲染控件 ←──────────┘
                                              ↓
用户输入 → SafetyManager 检查 → IceoryxBridge 发布
```

---

## 5. Proto 定义

### 5.1 OpenLoopCmd 消息

```protobuf
// 开环控制指令
message OpenLoopCmd {
  // 总开关
  bool enabled = 1;  // true: 开环控制生效, false: 开环控制禁用
  
  // 档位控制
  GearCommand gear_cmd = 2;  // P/R/N/D
  
  // 横向控制
  float steering_angle = 3;           // 方向盘角度 (°)
  float steering_angle_limit_pos = 4; // 角度限值 (正向, °)
  float steering_angle_limit_neg = 5; // 角度限值 (负向, °)
  
  // 纵向控制
  LongitudinalMode longitudinal_mode = 6;  // DISABLE/ACCEL/TORQUE
  float acceleration = 7;             // 加速度目标值 (m/s²)
  float acceleration_limit_pos = 8;   // 加速度限值 (正向, m/s²)
  float acceleration_limit_neg = 9;   // 加速度限值 (负向, m/s²)
  float torque = 10;                  // 扭矩目标值 (Nm, 正=油门, 负=刹车)
  float torque_limit_pos = 11;        // 扭矩限值 (油门, Nm)
  float torque_limit_neg = 12;        // 扭矩限值 (刹车, Nm)
  
  uint64 timestamp = 13;
}

enum GearCommand {
  GEAR_NONE = 0;
  GEAR_P = 1;
  GEAR_R = 2;
  GEAR_N = 3;
  GEAR_D = 4;
}

enum LongitudinalMode {
  LONGITUDINAL_DISABLE = 0;  // 关闭纵向控制
  LONGITUDINAL_ACCEL = 1;    // 加速度跟踪模式 (优先级高)
  LONGITUDINAL_TORQUE = 2;   // 扭矩跟踪模式
}
```

### 5.2 ControllerSignal 完整结构

```protobuf
message ControllerSignal {
  // ===== 提交类型标识 =====
  SubmitType submit_type = 1;  // 区分调参提交还是开环控制提交
  
  // ===== 调参字段 (submit_type = SUBMIT_TUNING 时生效) =====
  // PID 参数组
  message PIDParams {
    float kp = 1;
    float ki = 2;
    float kd = 3;
    bool integral_enabled = 4;
    float integrator_saturation = 5;
    bool derivative_enabled = 6;
  }
  PIDParams pid_0 = 2;  // PID 组 0
  PIDParams pid_1 = 3;  // PID 组 1
  PIDParams pid_2 = 4;  // PID 组 2
  PIDParams pid_3 = 5;  // PID 组 3
  
  // 扭矩表参数
  message TorqueTableEntry {
    float torque = 1;
    float gradient = 2;
  }
  repeated TorqueTableEntry torque_table = 6;  // 扭矩表 (15 个点位)
  
  // 坡道检测参数
  float pitch_gain_front_wheel_climbing = 7;   // 前轮爬坡增益
  float pitch_gain_rear_wheel_climbing = 8;    // 后轮爬坡增益
  float distance_threshold_to_stereo_lot_entrance_line = 9;
  float distance_offset_for_crossing = 10;
  float distance_offset_for_reset = 11;
  float slope_observe_range_start = 12;
  float slope_observe_range_end = 13;
  float slope_observe_threshold = 14;
  float slope_observe_distance_threshold = 15;
  float slope_observe_speed_threshold = 16;
  
  // 其他调参参数...
  float alpha_eta = 17;
  float alpha_eps = 18;
  float beta_eta = 19;
  float beta_eps = 20;
  float standstill_torque_margin = 21;
  float creep_start_up_torque = 22;
  float creep_moving_torque = 23;
  float max_rate_torque = 24;
  float dead_zone_torque = 25;
  float min_abs_brake_torque = 26;
  
  // ===== 开环控制指令 (submit_type = SUBMIT_OPEN_LOOP 时生效) =====
  OpenLoopCmd open_loop_cmd = 100;  // 开环控制指令
  
  uint64 timestamp = 200;
}

enum SubmitType {
  SUBMIT_NONE = 0;      // 无提交
  SUBMIT_TUNING = 1;    // 调参提交
  SUBMIT_OPEN_LOOP = 2; // 开环控制提交
}
```

---

## 6. UI 面板设计

### 6.1 整体布局

```
┌────────────────────────────────────────────────────────────────────┐
│  RACK Tool                                          □ ─ ×          │
├────────────────────────────────────────────────────────────────────┤
│                        MonitorPanel (监控面板)                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐  │  │
│  │  │  车辆状态       │  │  控制状态       │  │  安全状态       │  │  │
│  │  │  车速: 0.0 m/s │  │  模式: 调参    │  │  通信: 正常     │  │  │
│  │  │  方向盘: 0.0°  │  │  目标→实际    │  │  心跳: 正常     │  │  │
│  │  │  档位: P       │  │  跟踪误差      │  │  超时: 无       │  │  │
│  │  └────────────────┘  └────────────────┘  └────────────────┘  │  │
│  ├──────────────────────────────────────────────────────────────┤  │
│  │  ┌────────────────────────────┐  ┌────────────────────────┐  │  │
│  │  │  车速/加速度 曲线           │  │  方向盘/扭矩 曲线       │  │  │
│  │  └────────────────────────────┘  └────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────────┘  │
├────────────────────────────────────────────────────────────────────┤
│  [调参面板] [开环控制]                                               │
├────────────────────────────────────────────────────────────────────┤
│                     ParamsPanel / OpenLoopPanel                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │           (根据选中的标签页显示对应内容)                        │  │
│  └──────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────┘
```

### 6.2 调参面板 (ParamsPanel)

**布局:** 左右两列

```
┌─────────────────────────────────────────────────────────────────────────┐
│ 🔍 搜索参数...                            [提交] [重置] [保存]          │
├─────────────────────────────────────────────────────────────────────────┤
│ ┌──────────────────────────────┬──────────────────────────────────────┐ │
│ │ ▼ PID 参数组                 │ ▼ 扭矩表                             │ │
│ │   ├─ PID_0                   │   ├─ 点位 0                          │ │
│ │   │   Kp                     │   │   扭矩: [====●====] [-500.0]    │ │
│ │   │   [========●========]    │   │   梯度: [====●====] [2600.0]    │ │
│ │   │   [ 500.0 ]              │   ├─ 点位 1                          │ │
│ │   │   Ki                     │   │   扭矩: [====●====] [-250.0]    │ │
│ │   │   [========●========]    │   │   梯度: [====●====] [2200.0]    │ │
│ │   │   [ 50.0 ]               │   ├─ ...                             │ │
│ │   │   Kd                     │ ▼ 坡道检测参数                       │ │
│ │   │   [==================]   │   前轮增益: [====●====] [2.0]       │ │
│ │   │   [ 0.0 ]                │   后轮增益: [====●====] [1.5]       │ │
│ │   │   ☑ 积分 饱和:[100.0]    │   检测阈值: [====●====] [1.0]       │ │
│ │   │   □ 微分                 │                                      │ │
│ │   ├─ PID_1 ...               │                                      │ │
│ └──────────────────────────────┴──────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

**交互特性:**
- 滑动条支持键盘左右键微调
- 每个滑动条右侧有输入框，可直接输入精确值
- 输入值自动钳位到 [min, max] 范围
- 支持搜索过滤参数
- **批量提交模式**: 用户调节参数后，需点击 `[提交]` 按钮才下发到控制器
- `[重置]` 按钮：将所有参数和开环指令恢复到本次启动时的默认值
- `[保存]` 按钮：将当前参数保存到本地文件，下次启动自动加载

### 6.3 开环控制面板 (OpenLoopPanel)

**布局:** 左列（横向+档位），右列（纵向独占两列宽度）

```
┌─────────────────────────────────────────────────────────────────────────┐
│ ⚡ 开环控制使能: [==========●] ON                  [提交] [重置] [保存] │
├─────────────────────────────────────────────────────────────────────────┤
│ ┌───────────────────────────┬─────────────────────────────────────────┐ │
│ │    横向 + 档位控制         │              纵向控制                   │ │
│ ├───────────────────────────┼─────────────────────────────────────────┤ │
│ │                           │                                         │ │
│ │  目标方向盘角度 (°)        │    [ 关闭 | 加速度 | 扭矩 ]            │ │
│ │  ┌─────────────────────┐  │            当前: 关闭                   │ │
│ │  │ [========●========] │  │                                         │ │
│ │  └─────────────────────┘  │  ┌─────────────────────────────────────┐│ │
│ │  输入: [  0.0  ] °       │  │  加速度目标                          ││ │
│ │                           │  │  [============●============] 0.0   ││ │
│ │  角度限值                 │  │  输入: [  0.0  ] m/s²              ││ │
│ │  +[500]°  -[500]°        │  │  限值: +[3.0] -[3.0] m/s²          ││ │
│ │                           │  └─────────────────────────────────────┘│ │
│ ├───────────────────────────┤                                         │ │
│ │                           │  ┌─────────────────────────────────────┐│ │
│ │    [ P | R | N | D ]      │  │  扭矩目标                            ││ │
│ │       当前: P             │  │  [============●============] 0.0   ││ │
│ │                           │  │  输入: [  0.0  ] Nm                 ││ │
│ │                           │  │  限值: +[2600] -[4000] Nm           ││ │
│ │                           │  └─────────────────────────────────────┘│ │
│ └───────────────────────────┴─────────────────────────────────────────┘ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │                         [ 🛑 紧急停止 ]                              │ │
│ │                         下发 -4000 Nm 扭矩                           │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

**交互特性:**
- **开环控制使能开关**: 顶部滑动开关，OFF 时禁用所有开环控制，ON 时才生效
- 档位按钮：横向四段式，显示 `P | R | N | D`，下方显示当前档位
- 纵向模式按钮：横向三段式，显示 `关闭 | 加速度 | 扭矩`，下方显示当前模式
- 横向控制无独立启用开关，由总开关控制
- 加速度和扭矩各有独立的目标值控制条
- 纵向模式切换需二次确认
- **批量提交模式**: 用户调节后，需点击 `[提交]` 按钮才下发到控制器
- `[重置]` 按钮：将所有参数和开环指令恢复到本次启动时的默认值
- `[保存]` 按钮：将当前开环控制设置保存为默认值，下次启动自动加载
- 急停按钮：立即下发 -4000 扭矩，无需提交（自动关闭使能开关）

### 6.4 监控面板 (MonitorPanel)

**子面板:**
- 车辆状态：车速、方向盘角度、档位
- 控制状态：控制模式、目标值 vs 实际值、跟踪误差
- 安全状态：通信状态、心跳状态、超时计数

**曲线面板:**
- 车速/加速度曲线
- 方向盘/扭矩曲线

---

## 7. 安全机制

### 7.1 安全策略

| 机制 | 触发条件 | 行为 |
|------|----------|------|
| 心跳超时 | 订阅数据时间戳超过阈值 (默认 100ms) | 下发 -4000 扭矩 + P 档 |
| 急停按钮 | 用户点击 | 下发 -4000 扭矩刹停 |
| 限值保护 | 目标值超出限值 | 钳位到限值范围内 |
| 模式切换确认 | 切换纵向控制模式 | 弹出确认对话框 |

**提交模式：**

调参面板和开环控制面板均采用**批量提交模式**：
- 用户调节参数/指令后，需点击 `[提交]` 按钮才下发到控制器
- ControllerSignal 消息中包含 `submit_type` 字段，用于区分本次提交的类型

```protobuf
enum SubmitType {
  SUBMIT_NONE = 0;      // 无提交
  SUBMIT_TUNING = 1;    // 调参提交
  SUBMIT_OPEN_LOOP = 2; // 开环控制提交
}
```

**Controller 端处理逻辑：**
- 收到 `submit_type = SUBMIT_TUNING` 时，加载调参字段（PID、扭矩表等）
- 收到 `submit_type = SUBMIT_OPEN_LOOP` 时：
  - 若 `enabled = true`，执行开环控制（档位、方向盘、加速度/扭矩）
  - 若 `enabled = false`，忽略所有开环控制字段，保持控制器原有状态
- 收到 `submit_type = SUBMIT_NONE` 时，忽略本次消息

**按钮功能说明：**

| 按钮 | 功能 |
|------|------|
| `[提交]` | 将当前面板的参数/指令打包下发到控制器 |
| `[重置]` | 将所有参数和开环指令恢复到本次启动时的默认值 |
| `[保存]` | 将当前参数保存到本地文件，下次启动自动加载 |

**心跳检测机制：**

| 项目 | 说明 |
|------|------|
| 心跳源通道 | 使用 `ParkingChassis` 通道的时间戳作为心跳源 |
| 超时阈值 | 默认 100ms，可配置 |
| 启动行为 | 应用启动后，在收到第一帧 `ParkingChassis` 数据前，禁止提交任何开环控制指令 |
| 超时处理 | 心跳超时后自动下发安全指令（-4000 扭矩 + P 档），并禁用开环控制面板 |

### 7.2 默认限值

| 参数 | 正向限值 | 负向限值 |
|------|----------|----------|
| 方向盘角度 | +500° | -500° |
| 加速度 | +3.0 m/s² | -3.0 m/s² |
| 扭矩 | +2600 Nm (油门) | -4000 Nm (刹车) |

### 7.3 SafetyManager 接口

```cpp
class SafetyManager {
 public:
  // 检查并钳位指令
  bool CheckAndClamp(OpenLoopCmd& cmd);
  
  // 急停：下发 -4000 扭矩
  void EmergencyStop();
  
  // 心跳超时处理
  void OnHeartbeatTimeout();
  
  // 重置安全状态
  void Reset();
  
  // 设置心跳超时阈值
  void SetHeartbeatTimeout(std::chrono::milliseconds timeout);
  
 private:
  std::chrono::milliseconds heartbeat_timeout_{100};
  bool last_heartbeat_ok_{true};
  IceoryxBridge* bridge_;
};
```

---

## 8. Proto 反射引擎

### 8.1 功能

- 遍历 Proto 字段，提取字段名、类型、当前值
- 支持嵌套消息
- 支持 repeated 字段

### 8.2 接口

```cpp
struct FieldInfo {
  std::string path;           // "pid_params.kp"
  std::string display_name;   // "Kp" (来自 UI 配置)
  FieldType type;             // FLOAT/INT/BOOL/ENUM
  float current_value;
  float min_value;
  float max_value;
  float step;
};

class ProtoReflectionEngine {
 public:
  // 获取字段列表
  std::vector<FieldInfo> GetFieldValues(
      const google::protobuf::Message& msg, 
      const std::string& path);
  
  // 设置字段值
  bool SetFieldValue(
      google::protobuf::Message& msg, 
      const std::string& path, 
      float value);
  
  // 获取字段描述符
  const google::protobuf::FieldDescriptor* GetFieldDescriptor(
      const google::protobuf::Message& msg,
      const std::string& path);
};
```

### 8.3 UI 配置文件示例

```json
{
  "groups": [
    {
      "name": "PID 参数组",
      "path": "pid_params",
      "fields": [
        {
          "path": "pid_0.kp",
          "display_name": "PID_0 Kp",
          "min": 0.0,
          "max": 1000.0,
          "step": 1.0
        },
        {
          "path": "pid_0.ki",
          "display_name": "PID_0 Ki",
          "min": 0.0,
          "max": 500.0,
          "step": 1.0
        }
      ]
    },
    {
      "name": "扭矩表",
      "path": "torque_table",
      "repeated": true,
      "item_template": {
        "fields": [
          {"path": "torque", "display_name": "扭矩", "min": -500.0, "max": 500.0},
          {"path": "gradient", "display_name": "梯度", "min": 0.0, "max": 3000.0}
        ]
      }
    }
  ]
}
```

---

## 9. 监控信号扩展机制

### 9.1 扩展链路

```
1. 配置文件定义信号 (monitor_config.json)
                ↓
2. Proto 反射自动提取值
                ↓
3. DataContainer 存储时序数据
                ↓
4. ImPlot 绘制曲线
```

### 9.2 监控配置文件示例

```json
{
  "sub_panels": [
    {
      "name": "车辆状态",
      "signals": [
        {"path": "chassis.vehicle_speed", "display_name": "车速", "unit": "m/s"},
        {"path": "chassis.steering_angle", "display_name": "方向盘", "unit": "°"},
        {"path": "chassis.gear", "display_name": "档位", "type": "enum"}
      ]
    },
    {
      "name": "控制状态",
      "signals": [
        {"path": "control_cmd.target_value", "display_name": "目标值"},
        {"path": "control_cmd.actual_value", "display_name": "实际值"},
        {"path": "control_cmd.tracking_error", "display_name": "跟踪误差"}
      ]
    }
  ],
  "plot_groups": [
    {
      "name": "车速/加速度",
      "signals": ["chassis.vehicle_speed", "control_cmd.acceleration"],
      "time_window": 10.0
    },
    {
      "name": "方向盘/扭矩",
      "signals": ["chassis.steering_angle", "control_cmd.torque"],
      "time_window": 10.0
    }
  ]
}
```

### 9.3 新增信号步骤

1. 在 Proto 中定义新字段
2. 在 `monitor_config.json` 中配置信号路径和显示名称
3. 重新编译 Proto，无需修改 C++ 代码

---

## 10. 构建与运行

### 10.1 构建命令

```bash
# 编译
bazel build //mipilot/eng/parking/tools/rack_tool:launch_rack_tool_app

# 或使用脚本
./scripts/build_rack_tool.sh

# 打包部署
./scripts/build_rack_tool_tar.sh
```

### 10.2 运行命令

```bash
# 运行 (需要显示环境)
./scripts/rack_tool.sh
```

---

## 11. 依赖

| 依赖项 | 版本 | 用途 |
|--------|------|------|
| ImGui | 1.89+ | GUI 框架 |
| ImPlot | - | 曲线绘制 |
| GLFW | 3.x | 窗口管理 |
| OpenGL | 3.x | 渲染后端 |
| Iceoryx | - | 进程间通信 |
| ados::apprt | - | 应用框架 |
| Protobuf | - | 消息序列化 |

---

## 12. 风险与缓解

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| Proto 定义跨仓库同步 | 结构变更需三仓联动 | 使用共享 Proto 仓库，版本锁定 |
| 开环控制安全性 | 误操作可能导致危险 | 多重安全机制（心跳、急停、限值、确认） |
| ImGui DockSpace 兼容性 | 旧版本不支持 | 要求 ImGui 1.89+ |
| 屏幕适配兼容性 | 不同 DPI 显示器显示异常 | 使用物理像素计算，支持手动缩放调节 |
| 参数文件损坏 | 无法加载保存的参数 | 默认值兜底，文件损坏时自动重建 |

---

## 13. 屏幕自适应

### 13.1 自适应策略

| 屏幕尺寸 | 布局策略 | 字体缩放 |
|----------|----------|----------|
| 小屏 (<1280px 宽) | 单列布局，Tab 切换 | 0.8x |
| 中屏 (1280-1920px) | 双列布局 | 1.0x |
| 大屏 (>1920px) | 多列布局，扩展监控区 | 1.2x |

### 13.2 实现方式

```cpp
class ImGuiApp {
 private:
  void ApplyScreenAdaptation() {
    // 获取显示器尺寸
    GLFWmonitor* monitor = glfwGetPrimaryMonitor();
    const GLFWvidmode* mode = glfwGetVideoMode(monitor);
    int screen_width = mode->width;
    
    // 计算缩放比例
    float scale = 1.0f;
    if (screen_width < 1280) {
      scale = 0.8f;
    } else if (screen_width > 1920) {
      scale = 1.2f;
    }
    
    // 应用 ImGui 样式缩放
    ImGuiStyle& style = ImGui::GetStyle();
    style.ScaleAllSizes(scale);
    
    // 应用字体缩放
    ImGuiIO& io = ImGui::GetIO();
    io.FontGlobalScale = scale;
  }
  
  void OnWindowResize(int width, int height) {
    // 窗口大小变化时重新计算布局
    if (width < 1280) {
      layout_mode_ = LayoutMode::SINGLE_COLUMN;
    } else if (width < 1920) {
      layout_mode_ = LayoutMode::DUAL_COLUMN;
    } else {
      layout_mode_ = LayoutMode::EXPANDED;
    }
  }
};
```

---

## 14. 参数持久化

### 14.1 存储机制

| 项目 | 说明 |
|------|------|
| 存储位置 | `~/.config/rack_tool/saved_params.json` |
| 存储内容 | 调参参数 + 开环控制指令默认值 |
| 加载时机 | 应用启动时自动加载 |
| 保存时机 | 用户点击 `[保存]` 按钮 |

### 14.2 存储格式

```json
{
  "version": "1.0",
  "save_time": "2026-03-24T15:30:00",
  "tuning_params": {
    "pid_0": {
      "kp": 500.0,
      "ki": 50.0,
      "kd": 0.0,
      "integral_enabled": true,
      "integrator_saturation": 100.0,
      "derivative_enabled": false
    },
    "torque_table": [
      {"torque": -500.0, "gradient": 2600.0},
      {"torque": -250.0, "gradient": 2200.0}
    ],
    "slope_params": {
      "pitch_gain_front": 2.0,
      "pitch_gain_rear": 1.5
    }
  },
  "open_loop_defaults": {
    "enabled": false,
    "gear": "P",
    "steering_angle": 0.0,
    "steering_angle_limit_pos": 500.0,
    "steering_angle_limit_neg": 500.0,
    "longitudinal_mode": "DISABLE",
    "acceleration": 0.0,
    "acceleration_limit_pos": 3.0,
    "acceleration_limit_neg": 3.0,
    "torque": 0.0,
    "torque_limit_pos": 2600.0,
    "torque_limit_neg": 4000.0
  }
}
```

### 14.3 加载逻辑

```cpp
class ParamPersistence {
 public:
  // 加载保存的参数
  bool Load(ControllerSignal& signal);
  
  // 保存当前参数
  bool Save(const ControllerSignal& signal);
  
  // 获取存储路径
  std::string GetStoragePath() const;
  
 private:
  std::string storage_path_;
  bool has_saved_params_{false};
};

// 启动时加载
void RackToolApp::InitApp() {
  // 加载持久化参数
  if (persistence_.Load(controller_signal_)) {
    ADS_INFO << "Loaded saved parameters from " << persistence_.GetStoragePath();
  } else {
    ADS_INFO << "No saved parameters found, using defaults";
  }
}
```

### 14.4 重置逻辑

```cpp
// 重置到启动时的默认值
void RackToolApp::ResetToDefaults() {
  // 方式1: 如果有保存的参数，重置为保存的参数
  if (persistence_.has_saved_params()) {
    persistence_.Load(controller_signal_);
  } else {
    // 方式2: 否则重置为代码定义的默认值
    controller_signal_ = GetDefaultControllerSignal();
  }
}
```

---

## 15. 后续工作

1. 实现各模块代码
2. 集成测试
3. 与 `parking/controller` 联调
4. 性能优化
