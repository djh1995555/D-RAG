# 安装配件
1.  research-wiki：此后 /research-lit 自动入库论文，/idea-creator 读 wiki 再想 idea
```
/research-wiki init
```
1. 渐进式论文检索
```
pip install deepxiv-sdk
```
1. Exa AI 智能网页搜索
```
pip install exa-py
export EXA_API_KEY=adb737ad-0ef8-4d02-b4ed-0c3f6629a87f
```

  
# 安装

## claude code
安装：
```
bash ~/vibe/reference/ai-research/Auto-claude-code-research-in-sleep/tools/install_aris.sh
```
更新：
```
bash ~/vibe/reference/ai-research/Auto-claude-code-research-in-sleep/tools/install_aris.sh ~/your-paper-project
```

默认模式，用codex mcp进行review，用什么模型需要在`.codex/config.toml`中设置
```
"mcpServers": {
    "codex": {
      "args": [
        "mcp-server"
      ],
      "command": "codex",
      "env": {},
      "type": "stdio"
    }
}
```
## codex
### codex+codex(reviewer)

安装：
```
bash ~/vibe/reference/ai-research/Auto-claude-code-research-in-sleep/tools/install_aris_codex.sh .
```
更新：
```
bash ~/vibe/reference/ai-research/Auto-claude-code-research-in-sleep/tools/install_aris_codex.sh . --reconcile
```

### codex+claude(reviewer)

在工作目录下安装codex skill：
```
mkdir -p  .agents/skills/
cp -a ~/vibe/reference/ai-research/Auto-claude-code-research-in-sleep/skills/skills-codex/* .agents/skills/
```

设置claude review，注意skills是项目级的，mcp是用户级的

```
cp -a ~/vibe/reference/ai-research/Auto-claude-code-research-in-sleep/skills/skills-codex-claude-review/* .agents/skills/
mkdir -p ~/.codex/mcp-servers/claude-review
cp ~/vibe/reference/ai-research/Auto-claude-code-research-in-sleep/mcp-servers/claude-review/server.py ~/.codex/mcp-servers/claude-review/server.py
codex mcp add claude-review -- python3 ~/.codex/mcp-servers/claude-review/server.py
```
  
# 参数
| 参数                 | 默认         | 说明                                                                                                                             |
| ------------------ | ---------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `AUTO_PROCEED`     | `true`     | 在 idea 选择关卡自动继续。设为 `false` 可在花 GPU 前手动挑选 idea                                                                                  |
| `human checkpoint` | `false`    | 每轮 review 后暂停，让你查看分数、给出修改意见、跳过特定修复或提前终止                                                                                        |
| `sources`          | `all`      | 搜索哪些文献源：`zotero`、`obsidian`、`local`、`web`、`semantic-scholar`、`deepxiv`、`exa`、`all`。`semantic-scholar`、`deepxiv` 和 `exa` 都需显式指定 |
| `arxiv download`   | `false`    | 文献调研时下载最相关的 arXiv PDF。为 `false` 时仅获取元数据（标题、摘要、作者）                                                                              |
| `DBLP_BIBTEX`      | `true`     | 从 [DBLP](https://dblp.org)/[CrossRef](https://www.crossref.org) 获取真实 BibTeX，替代 LLM 生成。杜绝幻觉引用。零安装                               |
| `code review`      | `true`     | GPT-5.4 xhigh 部署前审查实验代码。设 `false` 跳过                                                                                           |
| `wandb`            | `false`    | 自动给实验脚本加 W&B 日志。设 `true` + 在 CLAUDE.md 配 `wandb_project`。`/monitor-experiment` 从 W&B 拉训练曲线                                     |
| `illustration`     | `gemini`   | 工作流 3 AI 作图：`gemini`（默认，需 `GEMINI_API_KEY`，[获取](https://aistudio.google.com/apikey)）、`mermaid`（免费）、`false`（跳过）                 |
| `venue`            | `ICLR`     | 目标会议：`ICLR`、`NeurIPS`、`ICML`、`CVPR`、`ACL`、`AAAI`、`ACM`、`IEEE_JOURNAL`、`IEEE_CONF`。决定 LaTeX 样式和页数限制                             |
| `base repo`        | `false`    | GitHub 仓库 URL，克隆作为实验基础代码（如 `— base repo: https://github.com/org/project`）。没有代码？基于开源项目开发                                        |
| `compact`          | `false`    | 生成精简摘要文件（`IDEA_CANDIDATES.md`、`findings.md`、`EXPERIMENT_LOG.md`），适合短 context 模型和 session 恢复                                    |
| `ref paper`        | `false`    | 参考论文（PDF 路径或 arXiv URL）。先总结论文，再基于它找 idea。配合 `base repo` 实现"论文+代码"工作流                                                           |
| `effort`           | `balanced` | 工作强度：`lite`(0.4x)、`balanced`(默认)、`max`(2.5x)、`beast`(5-8x)。Codex reasoning 永远 `xhigh`                                          |
| `reviewer`         | `codex`    | 审稿后端：`codex`（GPT-5.4 xhigh，默认）、`oracle-pro`（GPT-5.4 Pro via [Oracle](https://github.com/steipete/oracle)）                      |
| `difficulty`       | `medium`   | 审稿对抗强度：`medium`（默认）、`hard`（+ memory + 辩论）、`nightmare`（+ GPT 通过 `codex exec` 直读仓库）                                              |

```
/research-pipeline "你的课题" — AUTO_PROCEED: false                          # 在 idea 选择关卡暂停
/research-pipeline "你的课题" — human checkpoint: true                       # 每轮 review 后暂停，可给修改意见
/research-pipeline "你的课题" — sources: zotero, web                         # 只搜 Zotero + 网络（跳过本地 PDF）
/research-pipeline "你的课题" — sources: all, deepxiv                        # 默认源 + DeepXiv 渐进式检索
/research-pipeline "你的课题" — sources: all, exa                            # 默认源 + Exa AI 智能网页搜索
/research-pipeline "你的课题" — arxiv download: true                         # 文献调研时下载最相关的 arXiv PDF
/research-pipeline "你的课题" — difficulty: nightmare                        # 投顶会前极限压测
/research-pipeline "你的课题" — AUTO_PROCEED: false, human checkpoint: true  # 组合使用
```
# 完整流程 🚀

- **探索新方向（比如写 survey）？** 从工作流 1 开始 → `/idea-discovery`
	- `research-lit(调研文献)` + `idea-creator(找idea)` + `novelty-check(查新验证)` + `research-review(review方案)` + `research-refine-pipeline(打磨方案)`
- **有计划了，需要实现和跑实验？** 工作流 1.5 → `/experiment-bridge`
- **已有结果，需要迭代改进？** 工作流 2 → `/auto-review-loop`
- **准备写论文了？** 工作流 3 → `/paper-writing`（或分步：`/paper-plan` → `/paper-figure` → `/paper-write` → `/paper-compile` → `/auto-paper-improvement-loop`）
- **全流程？** 工作流 1 → 1.5 → 2 → 3 → `/research-pipeline`，从文献调研一路到投稿
- **想让 ARIS 记住并学习？** 📚 `/research-wiki init` — 跨会话持久记忆，论文、idea、失败实验复合积累
- **想让 ARIS 优化自己？** 工作流 M → `/meta-optimize` — 分析使用日志，提出技能改进，reviewer 审核

# 常用指令
`/idea-discovery "你的课题" — AUTO_PROCEED: false, human checkpoint: true`
