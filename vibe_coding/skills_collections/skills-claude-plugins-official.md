[anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official)

# Claude Code 官方插件列表

| 序号 | 功能 | 类型 | 名称 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| 1 | agent-sdk-dev | agents | agent-sdk-verifier-py | 使用此代理程序可验证 Python Agent SDK 应用程序是否已正确配置，是否遵循 SDK 最佳实践和文档建议，以及是否已准备好部署或测试。此代理程序应在创建或修改 Python Agent SDK 应用程序后调用。 |
| 2 | agent-sdk-dev | agents | agent-sdk-verifier-ts | 使用此代理程序可验证 TypeScript Agent SDK 应用程序是否已正确配置，是否遵循 SDK 最佳实践和文档建议，以及是否已准备好部署或测试。此代理程序应在创建或修改 TypeScript Agent SDK 应用程序后调用。 |
| 3 | agent-sdk-dev | commands | new-sdk-app | 创建和设置新的 Claude Agent SDK 应用程序。 |
| 4 | clangd-lsp | lsp | clangd | C/C++ 语言服务器，为 Claude Code 提供代码智能、诊断和格式化功能。支持扩展名：.c, .h, .cpp, .cc, .cxx, .hpp, .hxx, .C, .H |
| 5 | claude-code-setup | skill | - | 分析代码库并推荐定制的 Claude Code 自动化配置，如钩子、技能、MCP 服务器和子代理。 |
| 6 | claude-md-management | commands | revise-claude-md | 使用本会话的学习内容更新 CLAUDE.md。 |
| 7 | code-review | commands | code-review | 对 PR 进行代码审查。 |
| 8 | code-simplifier | agents | code-simplifier | 简化和优化代码以提高清晰度、一致性和可维护性，同时保留所有功能。专注于最近修改的代码，除非另有指示。 |
| 9 | commit-commands | commands | commit | 创建一个 git 提交。 |
| 10 | commit-commands | commands | commit-push-pr | 提交、推送并创建 PR。 |
| 11 | commit-commands | commands | clean_gone | 清理所有标记为 [gone] 的 git 分支（已从远程删除但仍存在于本地的分支），包括删除关联的工作树。 |
| 12 | csharp-lsp | lsp | csharp-ls | C# 语言服务器，为 Claude Code 提供代码智能和诊断功能。支持扩展名：.cs |
| 13 | example-plugin | commands | example-command | 一个示例斜杠命令，演示命令前置选项（旧版格式）。 |
| 14 | explanatory-output-style | hook | SessionStart | 自动在每个会话开始时添加指令，鼓励提供关于实现选择的见解并解释代码库模式和决策。 |
| 15 | feature-dev | agents | code-explorer | 通过跟踪执行路径、映射架构层、理解模式和抽象以及文档依赖关系来深度分析现有代码库功能，以指导新开发。 |
| 16 | feature-dev | agents | code-architect | 通过分析现有代码库模式和约定来设计功能架构，然后提供包含特定文件创建/修改、组件设计、数据流和构建序列的综合实现蓝图。 |
| 17 | feature-dev | agents | code-reviewer | 审查代码中的错误、逻辑错误、安全漏洞、代码质量问题以及对项目规范的遵守情况，使用基于置信度的过滤仅报告真正重要的优先问题。 |
| 18 | feature-dev | commands | feature-dev | 具有代码库理解和架构重点的引导式功能开发。 |
| 19 | frontend-design | skill | - | Claude 会自动将其用于前端工作，创建具有独特美学选择、大胆排版和配色方案的生产级代码。 |
| 20 | gopls-lsp | lsp | gopls | Go 语言服务器，为 Claude Code 提供代码智能、重构和分析功能。支持扩展名：.go |
| 21 | hookify | agents | conversation-analyzer | 分析对话转录以发现值得用钩子防止的行为。用于在没有参数的情况下运行 /hookify 命令或用户希望从最近的挫折中创建钩子时。 |
| 22 | hookify | commands | hookify | 创建钩子以防止对话分析或明确指令中的不良行为。 |
| 23 | hookify | commands | configure | 交互式启用或禁用 hookify 规则。 |
| 24 | hookify | commands | help | 获取 hookify 插件的帮助。 |
| 25 | hookify | commands | list | 列出所有已配置的 hookify 规则。 |
| 26 | jdtls-lsp | lsp | jdtls | Java 语言服务器（Eclipse JDT.LS），为 Claude Code 提供代码智能和重构功能。支持扩展名：.java |
| 27 | kotlin-lsp | lsp | kotlin-lsp | Kotlin 语言服务器，为 Claude Code 提供代码智能、重构和分析功能。支持扩展名：.kt, .kts |
| 28 | learning-output-style | hook | SessionStart | 自动激活交互式学习模式，在每个会话开始时添加指令，鼓励用户在决策点进行有意义的代码贡献。 |
| 29 | lua-lsp | lsp | lua-language-server | Lua 语言服务器，为 Claude Code 提供代码智能和诊断功能。支持扩展名：.lua |
| 30 | php-lsp | lsp | intelephense | PHP 语言服务器（Intelephense），为 Claude Code 提供代码智能和诊断功能。支持扩展名：.php |
| 31 | playground | skill | - | 创建交互式 HTML 游乐场——独立的单文件浏览器，具有可视化控件、实时预览和提示输出及复制按钮。 |
| 32 | plugin-dev | agents | agent-creator | 当用户要求"创建代理"、"生成代理"、"构建新代理"、"为我制作一个代理..."或描述他们需要的代理功能时使用。 |
| 33 | plugin-dev | agents | plugin-validator | 当用户要求"验证我的插件"、"检查插件结构"、"验证插件是否正确"、"验证 plugin.json"、"检查插件文件"或提及插件验证时使用。 |
| 34 | plugin-dev | agents | skill-reviewer | 当用户创建或修改技能并需要质量审查、要求"审查我的技能"、"检查技能质量"、"改进技能描述"或希望确保技能遵循最佳实践时使用。 |
| 35 | plugin-dev | commands | create-plugin | 具有组件设计、实现和验证的引导式端到端插件创建工作流。 |
| 36 | pr-review-toolkit | agents | code-reviewer | 审查代码是否符合项目指南、风格指南和最佳实践。应在编写或修改代码后主动使用，特别是在提交更改或创建 PR 之前。 |
| 37 | pr-review-toolkit | agents | comment-analyzer | 分析代码注释的准确性、完整性和长期可维护性。用于在完成大型文档注释后、在最终确定添加或修改注释的 PR 之前、在审查现有注释是否存在技术债务时使用。 |
| 38 | pr-review-toolkit | agents | type-design-analyzer | 专家分析代码库中的类型设计。用于在引入新类型时确保其遵循封装和不变量表达的最佳实践、在创建 PR 时审查所有添加的类型。 |
| 39 | pr-review-toolkit | agents | silent-failure-hunter | 审查 PR 中的代码更改以识别静默失败、不充分的错误处理和不适当的回退行为。应在完成涉及错误处理的代码后主动调用。 |
| 40 | pr-review-toolkit | agents | pr-test-analyzer | 审查 PR 的测试覆盖质量和完整性。应在创建或更新 PR 后调用，以确保测试充分覆盖新功能和边缘情况。 |
| 41 | pr-review-toolkit | agents | code-simplifier | 简化和优化代码以提高清晰度、一致性和可维护性，同时保留所有功能。应在代码编写或修改后自动触发。 |
| 42 | pr-review-toolkit | commands | review-pr | 使用专门的代理进行全面的 PR 审查。 |
| 43 | pyright-lsp | lsp | pyright | Python 语言服务器（Pyright），为 Claude Code 提供静态类型检查和代码智能功能。支持扩展名：.py, .pyi |
| 44 | ralph-loop | commands | ralph-loop | 在当前会话中启动 Ralph 循环，实现持续的自引用 AI 循环用于迭代式开发。 |
| 45 | ralph-loop | commands | cancel-ralph | 取消活动的 Ralph 循环。 |
| 46 | ralph-loop | commands | help | 解释 Ralph 循环插件和可用命令。 |
| 47 | ruby-lsp | lsp | ruby-lsp | Ruby 语言服务器，为 Claude Code 提供代码智能和分析功能。支持扩展名：.rb, .rake, .gemspec, .ru, .erb |
| 48 | rust-analyzer-lsp | lsp | rust-analyzer | Rust 语言服务器，为 Claude Code 提供代码智能和分析功能。支持扩展名：.rs |
| 49 | security-guidance | hook | PreToolUse | 安全提醒钩子，在编辑文件时警告潜在的安全问题，包括命令注入、XSS 和不安全的代码模式。 |
| 50 | skill-creator | skill | - | 创建新技能、改进现有技能并测量技能性能。用于创建技能、优化技能、运行测试或基准测试技能性能。 |
| 51 | swift-lsp | lsp | sourcekit-lsp | Swift 语言服务器（SourceKit-LSP），为 Claude Code 提供 Swift 项目的代码智能功能。支持扩展名：.swift |
| 52 | typescript-lsp | lsp | typescript-language-server | TypeScript/JavaScript 语言服务器，为 Claude Code 提供代码智能功能，如转到定义、查找引用和错误检查。支持扩展名：.ts, .tsx, .js, .jsx, .mts, .cts, .mjs, .cjs |



# 外部插件总览 (13个)

| 序号 | 名称 | 用途 | 开发者 | 触发方式 |
|:---:|------|------|--------|----------|
| [] | playwright | Microsoft 浏览器自动化和端到端测试 - 交互网页、截图、填表、点击元素 | Microsoft | "打开这个网页并截图", "自动化填写表单" |
| [] | context7 | Upstash Context7 MCP 服务器 - 获取最新文档和代码示例 | Upstash | "查找这个库的最新文档", "获取 React 的使用示例" |
| [] | asana | Asana 项目管理集成 - 创建和管理任务、搜索项目、更新分配、跟踪进度 | Asana | "创建一个新任务", "搜索 Asana 项目" |
| [] | supabase | Supabase MCP 集成 - 数据库操作、认证、存储和实时订阅 | Supabase | "执行 SQL 查询", "管理 Supabase 项目" |
| [] | greptile | AI 代码审查代理 - 查看和解决 Greptile 的 PR 审查评论 | Greptile | "查看 Greptile 的代码审查意见" |
| [] | serena | 语义代码分析 MCP 服务器 - 智能代码理解、重构建议、代码库导航 | Oraios | "分析这段代码", "查找代码中的问题" |
| [] | gitlab | GitLab DevOps 平台集成 - 管理仓库、MR、CI/CD、issue 和 wiki | GitLab | "查看我的 merge requests", "检查 CI/CD pipeline 状态" |
| [] | github | 官方 GitHub MCP 服务器 - 创建 issue、管理 PR、审查代码、搜索仓库 | GitHub | "创建一个 issue", "查看这个 PR 的状态", "搜索我的仓库" |
| [] | stripe | Stripe 开发插件 - 支付、webhook、API 和安全相关 | Stripe | "解释这个支付错误", "生成测试卡号" |
| [] | firebase | Google Firebase 集成 - 管理 Firestore、认证、云函数、托管和存储 | Google | "查询 Firestore 数据库", "管理 Firebase 认证" |
| [] | laravel-boost | Laravel 开发工具包 - Artisan 命令、Eloquent 查询、路由、迁移和代码生成 | Laravel | "创建一个 Laravel 迁移", "运行 Artisan 命令" |
| [] | slack | Slack 工作区集成 - 搜索消息、访问频道、读取讨论串 | Slack | "搜索 Slack 上的相关讨论", "查看这个频道的消息" |
| [] | linear | Linear 问题跟踪集成 - 创建 issue、管理项目、更新状态、搜索工作区 | Linear | "在 Linear 上创建一个 bug ticket", "更新这个任务的状态" |

---

*数据来源: /home/mi/.claude/plugins/marketplaces/claude-plugins-official/*
*生成时间: 2026-03-15*
