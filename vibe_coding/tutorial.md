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


# 优秀项目
- https://github.com/t3-oss/create-t3-app
- https://github.com/bytefer/awesome-nextjs



# 实战案例

* ☑️ [openclaw cases](https://github.com/hesamsheikh/awesome-openclaw-usecases)
* ☑️ [awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps)
* ☑️ [个人教程](https://adongwanai.github.io/)
