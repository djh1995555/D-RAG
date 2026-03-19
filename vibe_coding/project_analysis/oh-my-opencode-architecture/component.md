[TOC]
# 智能体

Oh-My-OpenCode 提供了 11 个专业 AI 智能体。每个智能体都有其独特的专业领域、优化的模型和工具权限。

## 核心智能体

| 智能体 | 模型 | 用途 |
| ----- |---- |------ |
| **Sisyphus** | `claude-opus-4-6` | 战略官。默认委托并使用专门的子智能体执行复杂任务，采用激进的并行执行方式。Todo 驱动的工作流，支持扩展思考（32k token 预算）。备选方案：`glm-5` → `big-pickle`。 |
| **Hephaestus** | `gpt-5.3-codex` | Hephaestus 运行于 GPT-5.3 Codex，当需要深度架构推理、跨多文件的复杂调试或跨领域知识合成时，给他一个目标，不用详细步骤，他会自己探索代码库、研究模式、端到端执行无需手把手指导。但是这个模式深度绑定GPT-CODEX，没有的话就别用了。备选方案：GitHub Copilot 上的 `gpt-5.4`。需要 GPT 能力提供商。 |
| **Oracle** | `gpt-5.4` | 高阶咨询。只在架构权衡、反复失败后的疑难杂症、重大技术决策时才请出来。只读、昂贵（推荐用 Opus）。备选方案：`gemini-3.1-pro` → `claude-opus-4-6`。 |
| **Librarian** | `gemini-3-flash` | 多代码库分析、文档查找、开源实现示例。深度代码库理解，基于证据的回答。备选方案：`minimax-m2.5-free` → `big-pickle`。 |
| **Explore** | `grok-code-fast-1` | 代码库检索专家。先分析你的意图，再并行调用搜索工具，最后给出结构化结果。备选方案：`minimax-m2.5-free` → `claude-haiku-4-5` → `gpt-5-nano`。 |
| **Multimodal-Looker** | `gpt-5.3-codex` | 视觉内容专家。分析 PDF、图片、图表以提取信息。备选方案：`k2p5` → `gemini-3-flash` → `glm-4.6v` → `gpt-5-nano`。 |

## 规划智能体

| 智能体 | 模型 | 用途 |
| ----- | ---- | ------ |
| **Prometheus** | `claude-opus-4-6` | 任务分解规划，支持访谈模式。通过迭代提问创建详细的工作计划。备选方案：`gpt-5.4` → `gemini-3.1-pro`。 |
| **Metis** | `claude-opus-4-6` | 规划顾问——在复杂任务里给 Prometheus 打辅助。它是只读的，不改任何东西，就是帮忙找出计划里可能有问题的地方。备选方案：`gpt-5.4` → `gemini-3.1-pro`。 |
| **Momus** | `gpt-5.4` | 规划审查器——它的定位是阻塞检查器，不是完美主义审稿器。默认偏向通过（OKAY），只有发现”真阻塞”才会拒绝（REJECT）。这个”默认通过”的设计很重要——如果审核太严，流水线会一直卡在审核环节转圈；如果太松，烂计划就会流到执行环节浪费 token。Momus 的平衡点是：只拦住那些会导致执行必定失败的问题。。备选方案：`claude-opus-4-6` → `gemini-3.1-pro`。 |

## 执行智能体

| 智能体 | 模型 | 用途 |
| ----- | --- | ---- |
| **Atlas** | `claude-sonnet-4-6` | 定位是 Conductor（总指挥），自己不写代码，只负责把计划拆成具体任务分发给执行者，然后验收结果。备选方案：`gpt-5.4`（medium）。 |
| **Sisyphus-Junior** | _(分类相关)_ | 具体执行。会根据任务分类（visual-engineering、quick、deep 等）自动选择设定好的模型。**特性**：无法将任务**重新委托**给其他智能体。**目的**：防止无限委托循环，确保专注于分配的任务。 |

### 任务委派模板
Atlas 和 Sisyphus 每次委派任务的时候，都要遵循一个固定的 6 段格式：
委托时，**清晰具体**的提示至关重要。包含以下 7 个要素：
```
1. **TASK**：需要做什么？（单一目标）
2. **EXPECTED OUTCOME**：交付物是什么？
3. **REQUIRED SKILLS**：应该通过 `load_skills` 加载哪些技能？
4. **REQUIRED TOOLS**：必须使用哪些工具？（白名单）
5. **MUST DO**：必须做什么（约束）
6. **MUST NOT DO**：绝不能做什么
7. **CONTEXT**：文件路径、现有模式、参考资料
```
**糟糕的示例**：

` "Fix this"`

**好的示例**：
```
 **TASK**: Fix mobile layout breaking issue in `LoginButton.tsx` 
 **CONTEXT**: `src/components/LoginButton.tsx`, using Tailwind CSS
 **MUST DO**: Change flex-direction at `md:` breakpoint
 **MUST NOT DO**: Modify existing desktop layout
 **EXPECTED**: Buttons align vertically on mobile
```
## 调用智能体

主智能体会自动调用这些智能体，但你也可以显式调用它们：

```
Ask @oracle to review this design and propose an architecture
Ask @librarian how this is implemented - why does the behavior keep changing?
Ask @explore for the policy on this feature
```

## 后台智能体

在后台运行智能体并继续工作：

- 让 GPT 调试的同时 Claude 尝试不同方法
- Gemini 编写前端而 Claude 处理后端
- 发起大规模并行搜索，继续实现，准备好时使用结果

```
# 在后台启动
task(subagent_type="explore", load_skills=[], prompt="Find auth implementations", run_in_background=true)

# 继续工作...
# 系统在完成时通知

# 需要时获取结果
background_output(task_id="bg_abc123")
```

## 智能体限制

| 智能体 | 限制 |
| ------ | ------ |
| oracle | 只读：无法写入、编辑或委托（阻止：write, edit, task, call_omo_agent） |
| librarian | 无法写入、编辑或委托（阻止：write, edit, task, call_omo_agent） |
| explore | 无法写入、编辑或委托（阻止：write, edit, task, call_omo_agent） |
| multimodal-looker | 白名单：仅允许 `read` |
| atlas | 无法委托（阻止：task, call_omo_agent） |
| momus | 无法写入、编辑或委托（阻止：write, edit, task） |


## 使用 Tmux 的可视化多智能体

启用 `tmux.enabled` 可以在独立的 tmux 窗格中查看后台智能体：

```json
{
  "tmux": {
    "enabled": true,
    "layout": "main-vertical"
  }
}
```

在 tmux 中运行时：

- 后台智能体在新窗格中生成
- 实时观看多个智能体工作
- 每个窗格实时显示智能体输出
- 智能体完成时自动清理

在 `oh-my-opencode.json` 中自定义智能体模型、提示和权限。

# 任务分类系统

任务分类是针对特定领域优化的智能体配置预设。与其将所有工作委托给单个AI智能体，根据任务的性质调用专门的智能体要高效得多。

## 什么是分类及其重要性

- **分类**："这是什么类型的工作？"（决定模型、温度、提示心态）
- **技能**："需要什么工具和知识？"（注入专门知识、MCP 工具、工作流）

通过结合这两个概念，你可以通过 `task` 生成最优的智能体。

## 内置分类

| 分类 | 默认模型 | 使用场景 |
| ----| ------- | ------ |
| `ultrabrain` | `openai/gpt-5.4` (xhigh) | 深度逻辑推理，需要广泛分析的复杂架构决策 |
| `deep` | `openai/gpt-5.3-codex` (medium) | 目标导向的自主问题解决。行动前深入研究。针对需要深度理解的有难度的问题。 |
| `quick` | `anthropic/claude-haiku-4-5` | 简单任务——单文件修改、拼写修正、简单修改 |
| `visual-engineering` | `google/gemini-3.1-pro` | 前端、UI/UX、设计、样式、动画 |
| `artistry` | `google/gemini-3.1-pro` (high) | 高度创意/艺术任务，新颖想法 |
| `writing` | `google/gemini-3-flash` | 文档、散文、技术写作 |
| `unspecified-low` | `anthropic/claude-sonnet-4-6` | 不适合其他分类的任务，低工作量 |
| `unspecified-high` | `anthropic/claude-opus-4-6` (max) | 不适合其他分类的任务，高工作量 |

## 自定义分类

你可以在 `oh-my-opencode.json` 中定义自定义分类。

### 分类配置 Schema

| 字段 | 类型 | 描述 |
| --- | ---- | ------- |
| `description` | string | 分类用途的人类可读描述。显示在任务提示中。 |
| `model` | string | 要使用的 AI 模型 ID（例如 `anthropic/claude-opus-4-6`） |
| `variant` | string | 模型变体（例如 `max`、`xhigh`） |
| `temperature` | number | 创造力级别（0.0 ~ 2.0）。越低越确定性。 |
| `top_p` | number | 核采样参数（0.0 ~ 1.0） |
| `prompt_append` | string | 选择此分类时追加到系统提示的内容 |
| `thinking` | object | 思考模型配置（`{ type: "enabled", budgetTokens: 16000 }`） |
| `reasoningEffort` | string | 推理努力级别（`low`、`medium`、`high`） |
| `textVerbosity` | string | 文本详细程度（`low`、`medium`、`high`） |
| `tools` | object | 工具使用控制（使用 `{ "tool_name": false }` 禁用） |
| `maxTokens` | number | 最大响应 token 数量 |
| `is_unstable_agent` | boolean | 将智能体标记为不稳定——强制后台模式以进行监控 |

### 配置示例

```jsonc
{
  "categories": {
    // 1. 定义新的自定义分类
    "korean-writer": {
      "model": "google/gemini-3-flash",
      "temperature": 0.5,
      "prompt_append": "You are a Korean technical writer. Maintain a friendly and clear tone.",
    },

    // 2. 覆盖现有分类（更改模型）
    "visual-engineering": {
      "model": "openai/gpt-5.4",
      "temperature": 0.8,
    },

    // 3. 配置思考模型并限制工具
    "deep-reasoning": {
      "model": "anthropic/claude-opus-4-6",
      "thinking": {
        "type": "enabled",
        "budgetTokens": 32000,
      },
      "tools": {
        "websearch_web_search_exa": false,
      },
    },
  },
}
```

# 技能

技能提供嵌入 MCP 服务器和详细指令的专业工作流。技能是一种机制，用于向智能体注入特定领域的**专门知识（上下文）**和**工具（MCP）**。

## 内置技能

| 技能 | 触发词 | 描述 |
| --- | ------| ----- |
| **git-master** | commit, rebase, squash, "who wrote", "when was X added" | Git 专家。检测提交风格，拆分原子提交，制定 rebase 策略。三种专业方向：提交架构师（原子提交、依赖排序、风格检测）、Rebase Surgeon（历史重写、冲突解决、分支清理）、历史考古学家（查找特定更改的引入时间和位置）。 |
| **playwright** | Browser tasks, testing, screenshots | 通过 Playwright MCP 进行浏览器自动化。必须用于浏览器验证、浏览、网页抓取、测试和截图。 |
| **playwright-cli** | Browser tasks on Playwright CLI | 通过 Playwright CLI 集成进行浏览器自动化。当更喜欢直接 CLI 脚本而非 MCP 时有用。 |
| **agent-browser** | Browser tasks on agent-browser | 通过 `agent-browser` CLI 进行浏览器自动化。涵盖导航、快照、截图、网络检查和脚本交互。 |
| **dev-browser** | Stateful browser scripting | 具有持久化页面状态的浏览器自动化，用于迭代工作流和认证会话。 |
| **frontend-ui-ux** | UI/UX tasks, styling | 设计师转开发者的角色。即使没有设计稿也能打造出色的 UI/UX。强调大胆的美学方向独特的字体、凝聚力的配色方案。 |

## git-master 核心原则

**默认多提交**：

```
3+ files -> 必须 2+ commits
5+ files -> 必须 3+ commits
10+ files -> 必须 5+ commits
```

**自动风格检测**：

- 分析最近 30 次提交的语言（韩语/英语）和风格（语义/普通/简短）
- 自动匹配你的仓库的提交约定

**使用**：

```
/git-master commit these changes
/git-master rebase onto main
/git-master who wrote this authentication code?
```

## frontend-ui-ux 设计流程

- **设计流程**：目的、风格、约束、差异化
- **美学方向**：选择极端风格——粗野主义、极繁主义、复古未来主义、奢华、活泼
- **字体**：独特的字体，避免通用字体（Inter、Roboto、Arial）
- **配色**：凝聚力的配色方案搭配尖锐的点缀，避免紫色背景白色文字的 AI 垃圾风格
- **动效**：高冲击力的交错揭示、滚动触发、令人惊喜的悬停状态
- **反模式**：通用字体、可预测的布局、模板化设计

## 浏览器自动化选项

Oh-My-OpenCode 提供两种浏览器自动化提供商，可通过 `browser_automation_engine.provider` 配置。

## 选项 1：Playwright MCP（默认）

```yaml
mcp:
  playwright:
    command: npx
    args: ["@playwright/mcp@latest"]
```

**使用**：

```
/playwright Navigate to example.com and take a screenshot
```

## 选项 2：Agent Browser CLI（Vercel）

```json
{
  "browser_automation_engine": {
    "provider": "agent-browser"
  }
}
```

**需要安装**：

```bash
bun add -g agent-browser
```

**使用**：

```
Use agent-browser to navigate to example.com and extract the main heading
```

**功能（两种提供商）**：

- 导航并与网页交互
- 截图和 PDF
- 填写表单和点击元素
- 等待网络请求
- 抓取内容

## 自定义技能创建（SKILL.md）

**技能加载位置**（优先级从高到低）：

- `.opencode/skills/*/SKILL.md`（项目，OpenCode 原生）
- `~/.config/opencode/skills/*/SKILL.md`（用户，OpenCode 原生）
- `.claude/skills/*/SKILL.md`（项目，Claude Code 兼容）
- `.agents/skills/*/SKILL.md`（项目，Agents 约定）
- `~/.agents/skills/*/SKILL.md`（用户，Agents 约定）

同名的技能优先级高的会覆盖优先级低的。

通过配置中的 `disabled_skills: ["playwright"]` 禁用内置技能。

你可以直接将自定义技能添加到上面的目录

## 分类 + 技能组合策略

你可以将分类和技能结合，创建强大的专门智能体。

### 设计师（UI 实现）

- **分类**：`visual-engineering`
- **load_skills**：`["frontend-ui-ux", "playwright"]`
- **效果**：实现美观的 UI 并直接在浏览器中验证渲染结果。

### 架构师（设计审查）

- **分类**：`ultrabrain`
- **load_skills**：`[]`（纯推理）
- **效果**：利用 GPT-5.4 xhigh 推理进行深入系统架构分析。

### 维护者（快速修复）

- **分类**：`quick`
- **load_skills**：`["git-master"]`
- **效果**：使用成本效益高的模型快速修复代码并生成干净的提交。



# 命令

命令是斜杠触发的工作流，执行预定义的模板。

## 内置命令

| 命令 | 描述 |
| --- | ----|
| `/init-deep` | 初始化分层 AGENTS.md 知识库 |
| `/ralph-loop` | 启动自引用开发循环直到完成 |
| `/ulw-loop` | 启动 ultrawork 循环——以 ultrawork 模式继续 |
| `/cancel-ralph` | 取消活动的 Ralph 循环 |
| `/refactor` | 智能重构，结合 LSP、AST-grep、架构分析和 TDD 验证 |
| `/start-work` | 从 Prometheus 计划启动 Sisyphus 工作会话 |
| `/stop-continuation` | 停止此会话的所有延续机制（ralph loop、todo continuation、boulder） |
| `/handoff` | 创建详细的上下文摘要，以便在新会话中继续工作 |

## /init-deep

**用途**：在项目中生成分层 AGENTS.md 文件

**使用**：

```
/init-deep [--create-new] [--max-depth=N]
```

创建目录特定的上下文文件，智能体会自动读取：

```
project/
├── AGENTS.md              # 首先注入
├── src/
│   ├── AGENTS.md          # 第二次注入
│   └── components/
│       ├── AGENTS.md      # 第三次注入
│       └── Button.tsx     # 读取此文件会注入全部 3 个
```

## /ralph-loop

**用途**：持续运行直到任务完成的自引用开发循环

**命名来源**：Anthropic 的 Ralph Wiggum 插件

**使用**：

```
/ralph-loop "Build a REST API with authentication"
/ralph-loop "Refactor the payment module" --max-iterations=50
```

**行为**：

- 智能体持续朝着目标工作
- 检测 `<promise>DONE</promise>` 知道何时完成
- 如果智能体停止而未完成则自动继续
- 结束条件：检测到完成、达到最大迭代次数（默认 100），或 `/cancel-ralph`

**配置**：`{ "ralph_loop": { "enabled": true, "default_max_iterations": 100 } }`

## /ulw-loop

**用途**：与 ralph-loop 相同，但激活 ultrawork 模式

一切以最大强度运行——并行智能体、后台任务、激进探索。

## /refactor

**用途**：使用完整工具链的智能重构

**使用**：

```
/refactor <target> [--scope=<file|module|project>] [--strategy=<safe|aggressive>]
```

**功能**：

- LSP 支持的重命名和导航
- AST-grep 模式匹配
- 更改前的架构分析
- 更改后的 TDD 验证
- Codemap 生成

## /start-work

**用途**：从 Prometheus 生成的计划开始执行

**使用**：

```
/start-work [plan-name]
```

使用 atlas 智能体系统化执行计划任务。

## /stop-continuation

**用途**：停止此会话的所有延续机制

停止 ralph loop、todo continuation 和 boulder 状态。当你想让智能体停止其当前多步骤工作流时使用。

## /handoff

**用途**：创建详细的上下文摘要以便在新会话中继续工作

生成结构化的交接文档，捕获当前状态、已完成的剩余的以及相关文件路径——实现无缝的新会话继续。

## 自定义命令

从以下位置加载自定义命令：

- `.opencode/command/*.md`（项目，OpenCode 原生）
- `~/.config/opencode/command/*.md`（用户，OpenCode 原生）
- `.claude/commands/*.md`（项目，Claude Code 兼容）
- `~/.config/opencode/commands/*.md`（用户，Claude Code 兼容）

# 工具

## 代码搜索工具

| 工具 | 描述 |
| --- | ---- |
| **grep** | 使用正则表达式的内容搜索。按文件模式过滤。 |
| **glob** | 快速文件模式匹配。按名称模式查找文件。 |

## 编辑工具

| 工具 | 描述 |
| ---- |---- |
| **edit** | 基于哈希的编辑工具。使用 `LINE#ID` 格式进行精确、安全的修改。在应用更改前验证内容哈希——零陈旧行错误。 |

## LSP 工具（智能体的 IDE 功能）

| 工具 | 描述 |
| ----| ---- |
| **lsp_diagnostics** | 获取构建前的错误/警告 |
| **lsp_prepare_rename** | 验证重命名操作 |
| **lsp_rename** | 跨工作区重命名符号 |
| **lsp_goto_definition** | 跳转到符号定义 |
| **lsp_find_references** | 查找跨工作区的所有引用 |
| **lsp_symbols** | 获取文件大纲或工作区符号搜索 |

## AST-Grep 工具

| 工具 | 描述 |
| --- | ---- |
| **ast_grep_search** | AST 感知的代码模式搜索（25 种语言） |
| **ast_grep_replace** | AST 感知的代码替换 |

## 委托工具

| 工具 | 描述 |
| ---- | ---- |
| **call_omo_agent** | 生成 explore/librarian 智能体。支持 `run_in_background`。 |
| **task** | 基于分类的任务委托。支持内置分类如 `visual-engineering`、`ultrabrain`、`deep`、`artistry`、`quick`、`unspecified-low`、`unspecified-high`、`writing`，或通过 `subagent_type` 直接定位智能体。 |
| **background_output** | 获取后台任务结果 |
| **background_cancel** | 取消运行中的后台任务 |

## 可视化分析工具

| 工具 | 描述 |
| ---- | ---- |
| **look_at** | 通过 Multimodal-Looker 智能体分析媒体文件（PDF、图片、图表）。从文档中提取特定信息或摘要，描述视觉内容。 |

## 技能工具

| 工具 | 描述 |
| ------------- | ------------------------------------------------------------------------------------------------------ |
| **skill** | 按名称加载和执行技能或斜杠命令。返回带有应用上下文的详细指令。 |
| **skill_mcp** | 调用技能嵌入的 MCP 服务器操作。 |

## 会话工具

| 工具 | 描述 |
| ------------------ | ---------------------------------------- |
| **session_list** | 列出所有 OpenCode 会话 |
| **session_read** | 从会话中读取消息和历史 |
| **session_search** | 跨会话消息全文搜索 |
| **session_info** | 获取会话元数据和统计 |

## 任务管理工具

需要在配置中启用 `experimental.task_system: true`。

| 工具 | 描述 |
| --------------- | ---------------------------------------- |
| **task_create** | 创建具有自动生成 ID 的新任务 |
| **task_get** | 按 ID 检索任务 |
| **task_list** | 列出所有活动任务 |
| **task_update** | 更新现有任务 |

## 交互式终端工具

| 工具 | 描述 |
| -------------------- | -------------------------------------------------------------------------------------------------- |
| **interactive_bash** | 基于 tmux 的 TUI 应用终端（vim、htop、pudb）。直接传递 tmux 子命令，无需前缀。 |

**使用示例**：

```bash
# 创建新会话
interactive_bash(tmux_command="new-session -d -s dev-app")

# 向会话发送按键
interactive_bash(tmux_command="send-keys -t dev-app 'vim main.py' Enter")

# 捕获窗格输出
interactive_bash(tmux_command="capture-pane -p -t dev-app")
```

**要点**：

- 命令是 tmux 子命令（无 `tmux` 前缀）
- 用于需要持久会话的交互式应用
- 一次性命令应使用常规 `Bash` 工具加 `&`

## 任务系统详情

**关于 Claude Code 对齐的说明**：此实现遵循 Claude Code 内部 Task 工具签名（`TaskCreate`、`TaskUpdate`、`TaskList`、`TaskGet`）和字段命名约定（`subject`、`blockedBy`、`blocks` 等）。然而，Anthropic 尚未发布这些工具的官方文档。这是 Oh My OpenCode 基于观察到的 Claude Code 行为和内部规范自行实现的。

**任务 Schema**：

```ts
interface Task {
  id: string; // T-{uuid}
  subject: string; // 祈使句："Run tests"
  description: string;
  status: "pending" | "in_progress" | "completed" | "deleted";
  activeForm?: string; // 现在进行时："Running tests"
  blocks: string[]; // 此任务阻塞的任务
  blockedBy: string[]; // 阻塞此任务的任务
  owner?: string; // 智能体名称
  metadata?: Record<string, unknown>;
  threadID: string; // 会话 ID（自动设置）
}
```

**依赖和并行执行**：

```
[Build Frontend]    ──┐
                      ├──→ [Integration Tests] ──→ [Deploy]
[Build Backend]     ──┘
```

- `blockedBy` 为空的任务并行运行
- 依赖任务等待阻塞任务完成

**示例工作流**：

```ts
TaskCreate({ subject: "Build frontend" }); // T-001
TaskCreate({ subject: "Build backend" }); // T-002
TaskCreate({ subject: "Run integration tests", blockedBy: ["T-001", "T-002"] }); // T-003

TaskList();
// T-001 [pending] Build frontend        blockedBy: []
// T-002 [pending] Build backend         blockedBy: []
// T-003 [pending] Integration tests     blockedBy: [T-001, T-002]

TaskUpdate({ id: "T-001", status: "completed" });
TaskUpdate({ id: "T-002", status: "completed" });
// T-003 现在解除阻塞
```

**存储**：任务以 JSON 文件形式存储在 `.sisyphus/tasks/`。

**与 TodoWrite 的区别**：

| 功能 | TodoWrite | 任务系统 |
| ------------------ | -------------- | -------------------------- |
| 存储 | 会话内存 | 文件系统 |
| 持久性 | 关闭时丢失 | 跨重启存活 |
| 依赖 | 无 | 完全支持（`blockedBy`） |
| 并行执行 | 手动 | 自动优化 |

**何时使用**：当工作有多个步骤且存在依赖关系、多个子智能体将协作、或进度需要跨会话持久化时。
# 钩子

钩子在智能体生命周期的关键点拦截并修改行为，贯穿整个会话、消息、工具和参数流程。

## 钩子事件

| 事件 | 时机 | 可以 |
| --- | --- | --- |
| **PreToolUse** | 工具执行前 | 阻止、修改输入、注入上下文 |
| **PostToolUse** | 工具执行后 | 添加警告、修改输出、注入消息 |
| **Message** | 消息处理期间 | 转换内容、检测关键词、激活模式 |
| **Event** | 会话生命周期变化时 | 恢复、回退、通知 |
| **Transform** | 上下文转换期间 | 注入上下文、验证块 |
| **Params** | 设置 API 参数时 | 调整模型设置、努力级别 |

## 内置钩子

## 上下文与注入

| 钩子 | 事件 | 描述 |
| ------------------------------- | ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **directory-agents-injector** | PreToolUse + PostToolUse | 读取文件时自动注入 AGENTS.md。从文件到项目根目录遍历，收集所有 AGENTS.md 文件。OpenCode 1.1.37+ 已弃用——原生 AGENTS.md 注入可用时自动禁用。 |
| **directory-readme-injector** | PreToolUse + PostToolUse | 自动注入 README.md 作为目录上下文。 |
| **rules-injector** | PreToolUse + PostToolUse | 条件匹配时从 `.claude/rules/` 注入规则。支持 glob 和 alwaysApply。 |
| **compaction-context-injector** | Event | 会话压缩时保留关键上下文。 |
| **context-window-monitor** | Event | 监控上下文窗口使用情况并跟踪 token 消耗。 |
| **preemptive-compaction** | Event | 在达到 token 限制前主动压缩会话。 |

## 生产力与控制

| 钩子 | 事件 | 描述 |
| --------------------------- | ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **keyword-detector** | Message + Transform | 检测关键词并激活模式：`ultrawork`/`ulw`（最高性能）、`search`/`find`（并行探索）、`analyze`/`investigate`（深度分析）。 |
| **think-mode** | Params | 自动检测扩展思考需求。捕获 "think deeply"、"ultrathink" 并调整模型设置。 |
| **ralph-loop** | Event + Message | 管理自引用循环继续。 |
| **start-work** | Message | 处理 /start-work 命令执行。 |
| **auto-slash-command** | Message | 自动执行提示中的斜杠命令。 |
| **gpt-permission-continuation** | Event | 当最终助手回复以寻求权限的尾部（如 `If you want, ...`）结束时自动继续 GPT 会话。 |
| **stop-continuation-guard** | Event + Message | 守护 stop-continuation 机制。 |
| **category-skill-reminder** | Event + PostToolUse | 提醒智能体有关可用于委托的分类技能。 |
| **anthropic-effort** | Params | 根据上下文调整 Anthropic API 努力级别。 |

## 质量与安全

| 钩子 | 事件 | 描述 |
| ------------------------------- | ------------------------ | ----------------------------------------------------------------------------------------- |
| **comment-checker** | PostToolUse | 提醒智能体减少过多注释。智能忽略 BDD、指令、文档字符串。 |
| **thinking-block-validator** | Transform | 验证思考块以防止 API 错误。 |
| **edit-error-recovery** | PostToolUse + Event | 从编辑工具故障中恢复。 |
| **write-existing-file-guard** | PreToolUse | 防止在未先读取的情况下意外覆盖现有文件。 |
| **hashline-read-enhancer** | PostToolUse | 为哈希行编辑工具增强读取输出，带有哈希锚定行标记。 |
| **hashline-edit-diff-enhancer** | PreToolUse + PostToolUse | 为哈希行编辑工具增强编辑操作，带有差异标记。 |

## 恢复与稳定性

| 钩子 | 事件 | 描述 |
| ------------------------------------------- | --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **session-recovery** | Event | 从会话错误中恢复——缺失的工具结果、思考块问题、空消息。 |
| **anthropic-context-window-limit-recovery** | Event | 优雅处理 Claude 上下文窗口限制。 |
| **runtime-fallback** | Event + Message | 在可重试的 API 错误（如 429、503、529）、提供商密钥配置错误（如缺少 API 密钥）和自动重试信号（当 `timeout_seconds > 0`）时自动切换到备份模型。可配置重试逻辑和每模型冷却时间。 |
| **model-fallback** | Event + Message | 当主模型不可用时管理模型回退链。 |
| **json-error-recovery** | PostToolUse | 从工具输出中的 JSON 解析错误中恢复。 |

## 截断与上下文管理

| 钩子 | 事件 | 描述 |
| ------------------------- | ----------- | --------------------------------------------------------------------------------------------------- |
| **tool-output-truncator** | PostToolUse | 截断 Grep、Glob、LSP、AST-grep 工具的输出。根据上下文窗口动态调整。 |

## 通知与用户体验

| 钩子 | 事件 | 描述 |
| ---------------------------- | ------------------- | -------------------------------------------------------------------------------------------------- |
| **auto-update-checker** | Event | 在会话创建时检查新版本，显示包含版本和 Sisyphus 状态的启动提示。 |
| **background-notification** | Event | 后台智能体任务完成时通知。 |
| **session-notification** | Event | 智能体空闲时发送操作系统通知。支持 macOS、Linux、Windows。 |
| **agent-usage-reminder** | PostToolUse + Event | 提醒你利用专门的智能体获得更好的结果。 |
| **question-label-truncator** | PreToolUse | 截断 Question 工具 UI 中的长问题标签。 |

## 任务管理

| 钩子 | 事件 | 描述 |
| -------------------------------- | ------------------- | --------------------------------------------------- |
| **task-resume-info** | PostToolUse | 提供任务恢复信息以保持连续性。 |
| **delegate-task-retry** | PostToolUse + Event | 重试失败的任务委托调用。 |
| **empty-task-response-detector** | PostToolUse | 检测委托任务的空响应。 |
| **tasks-todowrite-disabler** | PreToolUse | 任务系统激活时禁用 TodoWrite 工具。 |

## 延续

| 钩子 | 事件 | 描述 |
| ------------------------------ | ----- | ---------------------------------------------------------- |
| **gpt-permission-continuation** | Event | 继续以寻求权限尾部结束的 GPT 回复。 |
| **todo-continuation-enforcer** | Event | 强制执行 todo 完成——将空闲智能体拉回工作。 |
| **compaction-todo-preserver** | Event | 会话压缩时保留 todo 状态。 |
| **unstable-agent-babysitter** | Event | 使用恢复策略处理不稳定的智能体行为。 |

## 集成

| 钩子 | 事件 | 描述 |
| ---------------------------- | ------------------- | ------------------------------------------------------- |
| **claude-code-hooks** | All | 执行 Claude Code settings.json 中的钩子。 |
| **atlas** | Multiple | todo 驱动工作会话的主要编排逻辑。 |
| **interactive-bash-session** | PostToolUse + Event | 管理交互式 CLI 的 tmux 会话。 |
| **non-interactive-env** | PreToolUse | 处理非交互式环境约束。 |

## 专用

| 钩子 | 事件 | 描述 |
| --------------------------- | ---------- | -------------------------------------------------------- |
| **prometheus-md-only** | PreToolUse | 强制 Prometheus 规划器仅输出 markdown。 |
| **no-sisyphus-gpt** | Message | 防止 Sisyphus 在不兼容的 GPT 模型上运行。 |
| **no-hephaestus-non-gpt** | Message | 防止 Hephaestus 在非 GPT 模型上运行。 |
| **sisyphus-junior-notepad** | PreToolUse | 管理 Sisyphus-Junior 智能体的记事本状态。 |

## Claude Code 钩子集成

通过 Claude Code 的 `settings.json` 运行自定义脚本：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [{ "type": "command", "command": "eslint --fix $FILE" }]
      }
    ]
  }
}
```

**钩子位置**：

- `~/.claude/settings.json`（用户）
- `./.claude/settings.json`（项目）
- `./.claude/settings.local.json`（本地，git 忽略）

## 禁用钩子

在配置中禁用特定钩子：

```json
{
  "disabled_hooks": ["comment-checker", "gpt-permission-continuation"]
}
```

当你想让 GPT 会话在寻求权限的结尾处停止而不是自动恢复时，使用 `gpt-permission-continuation`。

# MCP

## 内置 MCP

| MCP | 描述 |
| ------------- | --------------------------------------------------------------------------------------------- |
| **websearch** | 由 Exa AI 驱动的实时网络搜索 |
| **context7** | 任何库/框架的官方文档查找 |
| **grep_app** | 跨公共 GitHub 仓库的超快速代码搜索。非常适合查找实现示例。 |

## 技能嵌入式 MCP

技能可以自带 MCP 服务器：

```yaml
---
description: Browser automation skill
mcp:
  playwright:
    command: npx
    args: ["-y", "@anthropic-ai/mcp-playwright"]
---
```

`skill_mcp` 工具使用完整的 schema 发现来调用这些操作。

## OAuth 启用 MCP

技能可以定义 OAuth 保护的远程 MCP 服务器。支持 OAuth 2.1 完整 RFC 合规性（RFC 9728、8414、8707、7591）：

```yaml
---
description: My API skill
mcp:
  my-api:
    url: https://api.example.com/mcp
    oauth:
      clientId: ${CLIENT_ID}
      scopes: ["read", "write"]
---
```

当技能 MCP 配置了 `oauth` 时：

- **自动发现**：获取 `/.well-known/oauth-protected-resource`（RFC 9728），回退到 `/.well-known/oauth-authorization-server`（RFC 8414）
- **动态客户端注册**：自动向支持 RFC 7591 的服务器注册（clientId 变为可选）
- **PKCE**：所有流程强制使用
- **资源指示符**：根据 RFC 8707 从 MCP URL 自动生成
- **令牌存储**：持久化到 `~/.config/opencode/mcp-oauth.json`（chmod 0600）
- **自动刷新**：令牌在 401 时刷新；403 时升级授权，带有 `WWW-Authenticate`
- **动态端口**：OAuth 回调服务器使用自动发现的可用端口

通过 CLI 预认证：

```bash
bunx oh-my-opencode mcp oauth login <server-name> --server-url https://api.example.com
```

# 上下文注入

## 目录 AGENTS.md

读取文件时自动注入 AGENTS.md。从文件目录遍历到项目根目录：

```
project/
├── AGENTS.md              # 首先注入
├── src/
│   ├── AGENTS.md          # 第二次注入
│   └── components/
│       ├── AGENTS.md      # 第三次注入
│       └── Button.tsx     # 读取此文件会注入全部 3 个
```

## 条件规则

条件匹配时从 `.claude/rules/` 注入规则：

```markdown
---
globs: ["*.ts", "src/**/*.js"]
description: "TypeScript/JavaScript coding rules"
---

- Use PascalCase for interface names
- Use camelCase for function names
```

支持：

- `.md` 和 `.mdc` 文件
- `globs` 字段用于模式匹配
- `alwaysApply: true` 用于无条件规则
- 从文件到项目根目录向上遍历，外加 `~/.claude/rules/`

# Claude Code 兼容性

Claude Code 配置的完整兼容层。

## 配置加载器

| 类型 | 位置 |
| ------------ | ---------------------------------------------------------------------------------- |
| **命令** | `~/.config/opencode/commands/`、`.claude/commands/` |
| **技能** | `~/.config/opencode/skills/*/SKILL.md`、`.claude/skills/*/SKILL.md` |
| **智能体** | `~/.config/opencode/agents/*.md`、`.claude/agents/*.md` |
| **MCP** | `~/.claude.json`、`~/.config/opencode/.mcp.json`、`.mcp.json`、`.claude/.mcp.json` |

MCP 配置支持环境变量扩展：`${VAR}`。

## 兼容性开关

禁用特定功能：

```json
{
  "claude_code": {
    "mcp": false,
    "commands": false,
    "skills": false,
    "agents": false,
    "hooks": false,
    "plugins": false
  }
}
```

| 开关 | 禁用 |
| ---------- | ------------------------------------------------------------ |
| `mcp` | `.mcp.json` 文件（保留内置 MCP） |
| `commands` | 从 Claude Code 路径加载命令 |
| `skills` | 从 Claude Code 路径加载技能 |
| `agents` | 从 Claude Code 路径加载智能体（保留内置智能体） |
| `hooks` | settings.json 钩子 |
| `plugins` | Claude Code 市场插件 |

禁用特定插件：

```json
{
  "claude_code": {
    "plugins_override": {
      "claude-mem@thedotmack": false
    }
  }
}
```

