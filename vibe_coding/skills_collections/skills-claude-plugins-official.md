# [Claude Plugins Official - 技能目录](https://github.com/anthropics/claude-plugins-official)

> 来源：claude-plugins-official/plugins

| 编号 | 功能 | 类型 | 名称 | 描述 | 路径 |
|------|------|------|------|------|------|
| 1 | agent-sdk-dev | agents | agent-sdk-verifier-py | Python Agent SDK 验证器 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/agent-sdk-dev/agents/agent-sdk-verifier-py.md |
| 2 | agent-sdk-dev | agents | agent-sdk-verifier-ts | TypeScript Agent SDK 验证器 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/agent-sdk-dev/agents/agent-sdk-verifier-ts.md |
| 3 | agent-sdk-dev | commands | new-sdk-app | 交互式命令，指导创建新的 Claude Agent SDK 应用程序 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/agent-sdk-dev/commands/new-sdk-app.md |
| 4 | clangd-lsp | skills | clangd-lsp | C/C++ 语言服务器，提供代码智能、诊断和格式化 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/clangd-lsp |
| 5 | claude-code-setup | skills | claude-automation-recommender | 分析代码库并推荐 Claude Code 自动化配置（MCP 服务器、技能、钩子、子代理、斜杠命令） | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/claude-code-setup/skills/claude-automation-recommender |
| 6 | claude-md-management | skills | claude-md-improver | 审计 CLAUDE.md 文件与当前代码库状态的一致性 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/claude-md-management/skills/claude-md-improver |
| 7 | claude-md-management | commands | revise-claude-md | 从当前会话中捕获学习内容并更新 CLAUDE.md | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/claude-md-management/commands/revise-claude-md.md |
| 8 | code-review | commands | code-review | 使用多个专业代理对 PR 进行自动化代码审查，带置信度评分过滤误报 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/code-review/commands/code-review.md |
| 9 | code-simplifier | agents | code-simplifier | 代码简化代理，用于审查和简化代码 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/code-simplifier/agents/code-simplifier.md |
| 10 | commit-commands | commands | commit | 创建 git 提交，自动生成基于暂存和未暂存更改的提交消息 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/commit-commands/commands/commit.md |
| 11 | commit-commands | commands | commit-push-pr | 完整工作流命令：提交、推送并在一步中创建 PR | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/commit-commands/commands/commit-push-pr.md |
| 12 | commit-commands | commands | clean_gone | 清理已删除分支的本地跟踪引用 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/commit-commands/commands/clean_gone.md |
| 13 | csharp-lsp | skills | csharp-lsp | C# 语言服务器，提供代码智能和诊断 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/csharp-lsp |
| 14 | example-plugin | skills | example-skill | 模型调用的技能示例（按任务上下文激活） | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/example-plugin/skills/example-skill |
| 15 | example-plugin | skills | example-command | 用户调用的技能示例（斜杠命令） | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/example-plugin/skills/example-command |
| 16 | example-plugin | commands | example-command | 遗留斜杠命令格式示例 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/example-plugin/commands/example-command.md |
| 17 | explanatory-output-style | skills | explanatory-output-style | 将废弃的 Explanatory 输出风格重现为 SessionStart 钩子，提供教育性洞察 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/explanatory-output-style |
| 18 | feature-dev | agents | code-architect | 代码架构师代理，负责架构设计 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/feature-dev/agents/code-architect.md |
| 19 | feature-dev | agents | code-explorer | 代码探索代理，负责代码库理解 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/feature-dev/agents/code-explorer.md |
| 20 | feature-dev | agents | code-reviewer | 代码审查代理，负责质量审查 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/feature-dev/agents/code-reviewer.md |
| 21 | feature-dev | commands | feature-dev | 启动引导式功能开发工作流，包含 7 个不同阶段 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/feature-dev/commands/feature-dev.md |
| 22 | frontend-design | skills | frontend-design | 生成独特、生产级的前端界面，避免通用 AI 美学 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/frontend-design/skills/frontend-design |
| 23 | gopls-lsp | skills | gopls-lsp | Go 语言服务器，提供代码智能、重构和分析 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/gopls-lsp |
| 24 | hookify | agents | conversation-analyzer | 对话分析代理，用于分析对话模式 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/hookify/agents/conversation-analyzer.md |
| 25 | hookify | skills | writing-rules | 编写规则的技能 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/hookify/skills/writing-rules |
| 26 | hookify | commands | hookify | 轻松创建自定义钩子以防止不良行为 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/hookify/commands/hookify.md |
| 27 | hookify | commands | configure | 配置 hookify 设置 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/hookify/commands/configure.md |
| 28 | hookify | commands | help | hookify 帮助命令 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/hookify/commands/help.md |
| 29 | hookify | commands | list | 列出所有 hookify 规则 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/hookify/commands/list.md |
| 30 | jdtls-lsp | skills | jdtls-lsp | Java 语言服务器（Eclipse JDT.LS），提供代码智能和重构 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/jdtls-lsp |
| 31 | kotlin-lsp | skills | kotlin-lsp | Kotlin 语言服务器，提供代码智能、重构和分析 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/kotlin-lsp |
| 32 | learning-output-style | skills | learning-output-style | 学习风格插件，结合交互式学习和教育洞察，让用户参与关键代码编写 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/learning-output-style |
| 33 | lua-lsp | skills | lua-lsp | Lua 语言服务器，提供代码智能和诊断 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/lua-lsp |
| 34 | math-olympiad | skills | math-olympiad | 带有对抗性验证的竞赛数学求解器，17/18 IMO+Putnam 2025 问题解决率 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/math-olympiad/skills/math-olympiad |
| 35 | mcp-server-dev | skills | build-mcp-server | MCP 服务器构建入口点，询问用例并选择部署模型 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/mcp-server-dev/skills/build-mcp-server |
| 36 | mcp-server-dev | skills | build-mcp-app | 添加在聊天中内联渲染的交互式 UI 小部件 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/mcp-server-dev/skills/build-mcp-app |
| 37 | mcp-server-dev | skills | build-mcpb | 将本地 stdio 服务器与其运行时打包，用户无需 Node/Python 即可安装 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/mcp-server-dev/skills/build-mcpb |
| 38 | php-lsp | skills | php-lsp | PHP 语言服务器（Intelephense），提供代码智能和诊断 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/php-lsp |
| 39 | playground | skills | playground | 创建交互式 HTML 游乐场——自包含单文件探索器，带有控件和实时预览 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/playground/skills/playground |
| 40 | plugin-dev | agents | agent-creator | AI 辅助生成代理的创建器 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/plugin-dev/agents/agent-creator.md |
| 41 | plugin-dev | agents | plugin-validator | 插件验证器代理 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/plugin-dev/agents/plugin-validator.md |
| 42 | plugin-dev | agents | skill-reviewer | 技能审查代理 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/plugin-dev/agents/skill-reviewer.md |
| 43 | plugin-dev | skills | agent-development | 创建具有 AI 辅助生成的自主代理 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/plugin-dev/skills/agent-development |
| 44 | plugin-dev | skills | command-development | 创建带有 frontmatter 和参数的斜杠命令 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/plugin-dev/skills/command-development |
| 45 | plugin-dev | skills | hook-development | 高级钩子 API 和事件驱动自动化 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/plugin-dev/skills/hook-development |
| 46 | plugin-dev | skills | mcp-integration | 模型上下文协议服务器集成 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/plugin-dev/skills/mcp-integration |
| 47 | plugin-dev | skills | plugin-settings | 使用 .claude/plugin-name.local.md 文件的配置模式 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/plugin-dev/skills/plugin-settings |
| 48 | plugin-dev | skills | plugin-structure | 插件组织和清单配置 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/plugin-dev/skills/plugin-structure |
| 49 | plugin-dev | skills | skill-development | 创建具有渐进式披露和强触发器的技能 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/plugin-dev/skills/skill-development |
| 50 | plugin-dev | commands | create-plugin | 从头创建插件的端到端工作流命令，8 阶段流程 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/plugin-dev/commands/create-plugin.md |
| 51 | pr-review-toolkit | agents | code-reviewer | PR 代码审查代理 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/pr-review-toolkit/agents/code-reviewer.md |
| 52 | pr-review-toolkit | agents | code-simplifier | 代码简化审查代理 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/pr-review-toolkit/agents/code-simplifier.md |
| 53 | pr-review-toolkit | agents | comment-analyzer | 代码注释准确性和可维护性分析代理 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/pr-review-toolkit/agents/comment-analyzer.md |
| 54 | pr-review-toolkit | agents | pr-test-analyzer | 测试覆盖质量和完整性分析代理 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/pr-review-toolkit/agents/pr-test-analyzer.md |
| 55 | pr-review-toolkit | agents | silent-failure-hunter | 静默失败检测代理 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/pr-review-toolkit/agents/silent-failure-hunter.md |
| 56 | pr-review-toolkit | agents | type-design-analyzer | 类型设计分析代理 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/pr-review-toolkit/agents/type-design-analyzer.md |
| 57 | pr-review-toolkit | commands | review-pr | PR 审查命令 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/pr-review-toolkit/commands/review-pr.md |
| 58 | pyright-lsp | skills | pyright-lsp | Python 语言服务器（Pyright），提供静态类型检查和代码智能 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/pyright-lsp |
| 59 | ralph-loop | commands | ralph-loop | 实现 Ralph Wiggum 技术用于迭代自引用 AI 开发循环 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/ralph-loop/commands/ralph-loop.md |
| 60 | ralph-loop | commands | cancel-ralph | 取消 Ralph 循环 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/ralph-loop/commands/cancel-ralph.md |
| 61 | ralph-loop | commands | help | Ralph Loop 帮助命令 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/ralph-loop/commands/help.md |
| 62 | ruby-lsp | skills | ruby-lsp | Ruby 语言服务器，提供代码智能和分析 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/ruby-lsp |
| 63 | rust-analyzer-lsp | skills | rust-analyzer-lsp | Rust 语言服务器，提供代码智能和分析 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/rust-analyzer-lsp |
| 64 | security-guidance | skills | security-guidance | 安全指导钩子，提供安全相关提醒 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/security-guidance |
| 65 | skill-creator | skills | skill-creator | 创建新技能、改进现有技能并衡量技能性能 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/skill-creator/skills/skill-creator |
| 66 | swift-lsp | skills | swift-lsp | Swift 语言服务器（SourceKit-LSP），提供 Swift 项目的代码智能 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/swift-lsp |
| 67 | typescript-lsp | skills | typescript-lsp | TypeScript/JavaScript 语言服务器，提供代码智能功能 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/typescript-lsp |

## 统计

- 总计：67 项
- agents：14 项
- commands：19 项
- skills：34 项
