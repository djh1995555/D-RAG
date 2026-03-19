[TOC]
# 工具
| 概念 | 谁触发 | 最适合的场景 | 上下文成本 | 常见反模式 |
|------|--------|--------------|------------|------------|
| **Rules** | 系统/LLM 自动匹配 | 全局约束、格式规范、禁止行为、基础话术 | 高（每次请求都会读取） | 把教程、长逻辑、复杂流程塞进规则里 |
| **Subagents** | 主Agent 调度 | 复杂任务拆解、专业领域分工、长流程协作 | 中高（独立上下文/状态） | 过度拆分、通信成本高、调度逻辑混乱 |
| **Skills** | 用户意图/关键词匹配 | 单轮技能、固定任务、可复用能力 | 中（按需加载） | 拆得太碎、技能互相冲突、依赖复杂上下文 |
| **Commands** | 用户显式输入指令 | 明确操作、快捷功能、确定性执行 | 低（指令解析+执行） | 命令过多、语义模糊、和技能边界不清 |
| **Mcp** | 工具调用/Agent 调度 | 外部服务、数据查询、插件扩展、IO 操作 | 低（调用即执行，无上下文残留） | 把业务逻辑写在 Mcp 里、过度封装简单逻辑 |
| **Hooks** | 生命周期事件 | 请求前/后处理、埋点、鉴权、日志、拦截 | 极低（切面执行，不占prompt） | 业务逻辑写进 Hook、影响主流程 |

## [Rules](https://github.com/flyeric0212/cursor-rules/tree/main)
rules不应该全部写在CLAUDE.md里面，应该要拆分成小文件，在需要的时候再读取
### **交互规则**
- 请用中文回答我
- 修改文件前是否必须询问
- 批量修改的限制
- 自动保存的配置

### **项目概述**
- 项目名称和目的
- 技术栈
- 架构
- 项目结构说明，每个部分是干什么的

### **可用资源**
- Skills
- Subagents
- Mcp
- 第三方库，组件，框架

### **开发环境设置**
- 如何安装依赖
- 如何启动开发服务器
- 必要的配置步骤

### **构建**
- 构建命令

### **测试**
- 测试命令
- 测试框架
- 覆盖率期望
- 断言风格
- mock 方案

### 代码审查
- 代码检查
- 代码格式化
- 内存性能检查

### **常用命令**
- 项目特定的 CLI 命令
- 常用的脚本

### **git规范**
- git commit规范
- 是否自动提交
- 分支管理策略

### **代码风格**
- 遵循《代码整洁之道》
- 避免不必要的对象复制或克隆
- 避免多层嵌套，提前返回
- 使用适当的并发控制机制
- 如果回答的是代码，请给每个关键节点，比较难懂的代码增加中文注释
- 当生成的代码行数超过 20 行时，请考虑聚合代码以及考虑其颗粒度是否适合
- 编写可测试的代码
- 避免重复代码
- 优先考虑现有的库和工具，不要重复造轮子
- 始终考虑代码的可维护性和可扩展性

### **错误处理**
- 用 Result 类型还是 try/catch
- 日志怎么打
- 参数验证用什么方案

### **全局约束**
- 强制性的行为边界
- 禁止的操作（如：禁止直接操作生产数据库）
- 必须遵守的安全规范

### **输出文档格式**
- 目录结构
- 版本记录规范


### 与 CLAUDE.md 的区别

| rules.md | CLAUDE.md |
|----------|-----------|
| AI 行为约束和规范 | 项目文档和上下文 |
| 告诉 AI "应该怎么做" | 告诉 AI "项目是什么" |
| 适用于任何项目 | 特定于当前项目 |
| 相对固定、通用 | 随项目变化 |

## Subagents
Subagents.md需要包含以下部分
- Frontmatter
```
---
name: code-reviewer
description: Reviews code for quality and best practices
tools: Read, Glob, Grep
model: sonnet
---
```
| Field | Required | Description |
|-------|----------|-------------|
| name | Yes | 使用小写字母和连字符的唯一标识符 |
| description | Yes | Claude 何时应委托给此 subagent |
| tools | No | Subagent 可以使用的 Tools。如果省略，继承所有工具 |
| disallowedTools | No | 要拒绝的工具，从继承或指定的列表中删除 |
| model | No | 要使用的 Model：sonnet、opus、haiku 或 inherit。默认为 inherit |
| permissionMode | No | Permission mode：default、acceptEdits、dontAsk、bypassPermissions 或 plan |
| maxTurns | No | subagent 停止前的最大代理轮数 |
| skills | No | 在启动时加载到 subagent 上下文中的 Skills。注入完整的技能内容，而不仅仅是可用于调用。Subagents 不继承父对话中的技能 |
| mcpServers | No | 此 subagent 可用的 MCP servers。每个条目要么是引用已配置服务器的服务器名称（例如 "slack"），要么是内联定义，其中服务器名称为键，完整的 MCP server config 为值 |
| hooks | No | 限定于此 subagent 的 Lifecycle hooks |
| memory | No | Persistent memory scope：user、project 或 local。启用跨会话学习 |
| background | No | 设置为 true 以始终将此 subagent 作为 background task 运行。默认值：false |
| isolation | No | 设置为 worktree 以在临时 git worktree 中运行 subagent，为其提供存储库的隔离副本。如果 subagent 不进行任何更改，worktree 会自动清理 |
- agents功能，和Frontmatter里的description差不多
- agents设定
- 具体任务
- 遵守的规则
- 任务相关知识，可用的skill，mcp，第三方库，框架，组件等等
- 工作流程
- 交付成果标准，或者直接给个示例
- 学习和记忆，能够记住自己的产出
- 成功指标
总的来说，没有非常严格的标准要写什么
## Skills
## Commands
## Mcp
## Hooks

# 流程
- [确定技术栈](VibeCoding/reference/technical_stack.md)
	- 前端：Next.js
	- 后端：FastAPI
	- UI组件：Tailwind V4和Shadcn ui
	- 数据库：PostgreSQL和Redias
	- 前端部署：Vercel
	- 后端部署：supabase
- spec：需求分析，制定计划，拆分任务，这里每一步如果能拆分的话，也需要用别的agent来review，循环几次，完善计划
- 搭建项目架构
- 测试驱动开发+review
  - 先写测试，再开发
  - 测试方案出来，也可以用另一个agent去review
  - 测试设计，测试review，开发，开发review分别用不同的agents
- 端到端测试
- 内存性能优化
- 文档更新
- 代码质量
  - 设置hook，在每次写完代码，自动运行风格化
  - 单元测试和端到端测试
  - code review
  - pre-commit hook：提交前操作自动化
  - github ci/cd



# 前端
## 资源
### 图标
- lucide
### 组件库
- [ui：成熟ui库](https://github.com/shadcn-ui/ui)
- [tailwindcss：成熟ui库](https://github.com/tailwindlabs/tailwindcss)
- tweakcn：可视化调色板
- MagicUI：动画组件
- AceternityUI：特效专家
- 21 st.dev：shadcn兼容组件库（有mcp）
### 参考网站
- [dribbble：都有](https://dribbble.com/shots/popular/mobile)
- [layers：都有](https://layers.to/explore)
- [awwwards：都有](https://www.awwwards.com/)
- [mobbin：移动端](https://mobbin.com/)
- [ui pocket：移动端](https://www.ui-pocket.com/mobile)
- [60fps：移动端动效](https://60fps.design/)
- [landing.love：网页动画](https://www.landing.love/)
- [godly.website：网页端](https://godly.website/)
- [即时设计](https://js.design/community?category=explore)
## 关键点
### 布局和结构
- 网格布局
- 弹性布局
- 响应式布局
- 便当盒布局
- 瀑布流布局
- 粘性侧边栏/顶栏
### 视觉和质感
- 毛玻璃/玻璃拟态
- 粘土拟态
- 极光渐变
### 交互和动效
- 视差滚动（滚动时，背景动得慢，文字动得快）
- 

## UI设计提示词
```
	1.视觉风格：
	-背景色：背景使用深色，边框采用极细的半透明
	白色。
	一品牌色：核心品牌色为荧光绿（a7f069)。请将其
	用于图标颜色、边框的高亮态，以及悬停时的渐变
	光晕。
	-文字色：标题文字使用纯白，描述文字使用略带
	透明度的灰色以形成层级感。
	-圆角：卡片采用24px的大圆角。
	2.内容布局：
	一垂直结构：由上至下依次为图标、标题、描述。
	一图标容器：图标需包裹在一个带1px细边框的深
	色圆角方块内。
	3.交互动效(重点）：
	-荧光弥散光晕：当鼠标Hover时，卡片背后需出
	现一层以荧光绿为主色的弥散光晕（Blur效果），
	模拟霓虹背光的感觉。
	一微位移反馈：悬停时卡片平滑上浮4px，同时内
	部的图标容器微调放大（Scale 110%）。
	-平滑过渡：所有颜色和位移的变化均需设定为
	0.3s-0.5s的过渡时间。
```



# 全栈项目
## 项目结构
### 1. Monorepo 结构（推荐）
```
my-project/
├── apps/                        # 应用目录（按业务维度拆分）
│   ├── web/                     # 前端应用（React/Vue 等）
│   │   ├── src/
│   │   │   ├── components/      # 业务 UI 组件
│   │   │   ├── pages/           # 页面/路由组件
│   │   │   ├── hooks/           # 自定义 React Hooks
│   │   │   ├── stores/          # 状态管理（Pinia/Redux 等）
│   │   │   └── utils/           # 前端工具函数
│   │   ├── package.json         # 前端依赖配置
│   │   └── vite.config.ts       # 前端构建配置
│   │
│   └── api/                     # 后端应用（Node.js/Java 等）
│       ├── src/
│       │   ├── controllers/     # 接口控制器（处理请求/响应）
│       │   ├── services/        # 核心业务逻辑层
│       │   ├── models/          # 数据模型/实体
│       │   ├── routes/          # 路由定义
│       │   ├── middleware/      # 中间件（鉴权/日志等）
│       │   ├── config/          # 环境配置/常量
│       │   └── utils/           # 后端工具函数
│       ├── package.json         # 后端依赖配置
│       └── tsconfig.json        # TypeScript 配置
│
├── packages/                    # 跨应用共享包（可独立发布）
│   ├── shared-types/            # 前后端共享 TypeScript 类型
│   ├── database/                # 数据库公共逻辑（ORM/迁移/连接）
│   └── ui/                      # 跨项目共享 UI 组件库
│
├── docker-compose.yml           # 基础设施编排（数据库/缓存等）
├── package.json                 # 根级依赖/脚本（如 turbo 命令）
└── turbo.json                   # Monorepo 任务调度配置（TurboRepo）
```

### 2. 分离式结构（传统拆分）
```
my-project/
├── frontend/                    # 前端项目（独立仓库等价物）
│   ├── public/                  # 静态资源
│   ├── src/                     # 前端源码
│   ├── package.json             # 前端依赖
│   └── Dockerfile               # 前端容器构建
│
├── backend/                     # 后端项目（独立仓库等价物）
│   ├── src/                     # 后端源码
│   ├── tests/                   # 后端单元/集成测试
│   ├── package.json             # 后端依赖
│   └── Dockerfile               # 后端容器构建
│
├── database/                    # 数据库独立管理
│   ├── migrations/              # 数据库迁移脚本
│   ├── seeds/                   # 测试数据/初始化数据
│   └── docker-compose.yml       # 数据库单机部署配置
│
├── nginx/                       # Nginx 反向代理/静态资源配置
│   ├── nginx.conf               # 核心配置
│   └── default.conf             # 站点配置
│
├── docker-compose.yml           # 整体服务编排（前端+后端+数据库+Nginx）
└── README.md                    # 项目整体说明
```

# 优秀项目
- https://github.com/t3-oss/create-t3-app
- https://github.com/bytefer/awesome-nextjs