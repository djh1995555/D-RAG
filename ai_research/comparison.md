# AI 自动化研究框架对比分析

> 分析日期：2026-04-23
> 仓库来源：repos.md 中列出的 5 个项目

---

## 1. 项目概览

| 项目 | 开发者 | 核心理念 | 仓库 |
|------|--------|---------|------|
| **ARIS** (Auto-claude-code-research-in-sleep) | wanshuiyin (个人) | "睡觉时做研究"的完整ML研究流水线 | [GitHub](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) |
| **autoresearch** | Andrej Karpathy | 让AI自主优化LLM预训练代码 | [GitHub](https://github.com/karpathy/autoresearch) |
| **AI-Scientist-v2** | Sakana AI | 端到端自主科学发现，首个AI通过同行评审的论文 | [GitHub](https://github.com/SakanaAI/AI-Scientist-v2) |
| **Alchemy** | 清华大学软件所 | 闭环迭代优化ML算法 | [GitHub](https://github.com/TsinghuaISE/Alchemy) |
| **AI-Researcher** | 港大数据科学实验室 | 多Agent协作的科研发现框架 | [GitHub](https://github.com/HKUDS/AI-Researcher) |

---

## 2. 核心维度对比

| 维度 | ARIS | autoresearch | AI-Scientist-v2 | Alchemy | AI-Researcher |
|------|------|-------------|----------------|---------|--------------|
| **研究范围** | ML/NLP (通用，支持理论/实证/方法/调研) | 仅LLM预训练 (极窄领域) | ML实验 (多种子领域) | 时序预测 + 推荐系统 | ML (VQ/GNN/扩散/推理/推荐) |
| **自动化程度** | 全自主 + 可配置人工检查点 | 全自主 (仅启动时需人工) | 全自主 (需提供初始主题) | 全自主 (需提供种子基线) | 高度自主 (需提供任务/参考论文) |
| **LLM后端** | Claude Code + 多模型审查 (GPT/DeepSeek/Gemini等) | 模型无关 (任何编码Agent) | Claude/GPT-4o/Gemini/DeepSeek/本地 | Gemini 3 Flash (可配置) | GPT-4o / GPT-4o-mini (litellm) |
| **Agent架构** | 单Agent + MCP工具 + 多模型审查 | 单Agent + program.md指令 | 树搜索 (BFTS) + 并行Agent | 单Agent循环 + 多温度采样 | 7+专用Agent + 交接机制 |
| **搜索策略** | 线性流水线+审查循环 | 贪心 (只保留改进) | 最佳优先树搜索 (BFTS) | 迭代循环+耐心机制 | 线性流水线+Judge迭代 |
| **代码规模** | 大 (73+ skill目录, 155KB README) | 极小 (4个核心文件) | 中等 (多模块) | 中等 (2大子系统) | 大 (多Agent+论文子系统) |

---

## 3. 研究流程对比

| 功能模块 | ARIS | autoresearch | AI-Scientist-v2 | Alchemy | AI-Researcher |
|---------|------|-------------|----------------|---------|--------------|
| **文献调研** | ✅ 多源 (arXiv/S2/DeepXiv/Exa/Zotero/Obsidian) | ❌ 无 | ✅ Semantic Scholar集成 | ❌ 无 (仅预存知识文件) | ✅ arXiv下载 + GitHub代码搜索 |
| **创意生成** | ✅ 8-12个创意→可行性/新颖性过滤→试点实验 | ❌ 无 (人工给定方向) | ✅ LLM头脑风暴+多轮反思+新颖性检查 | ⚠️ 假设生成 (基于种子代码修改) | ✅ 5轮迭代生成最佳创意 |
| **代码生成** | ✅ PyTorch/JAX实验脚本+评估+绘图 | ✅ 仅修改train.py | ✅ 完整Python实验代码 | ✅ 算法代码修改+超参YAML | ✅ 完整PyTorch项目结构 |
| **实验执行** | ✅ 多GPU (本地/SSH/Vast.ai/Modal) + 队列调度 | ✅ 单GPU 5分钟固定预算 | ✅ 沙箱执行+自动调试 | ✅ Docker/Singularity+多GPU (32并发) | ✅ Docker+GPU容器隔离 |
| **实验管理** | ✅ 队列编排+OOM重试+波次过渡+状态持久化 | ✅ Git提交追踪+结果TSV | ✅ 树搜索日志+可视化HTML | ✅ 实时终端展示+摘要JSON | ✅ 迭代修正循环+Judge评估 |
| **论文写作** | ✅ 逐节LaTeX+多会议模板+5轮写作审计 | ❌ 无 | ✅ 完整LaTeX+Semantic Scholar引用 | ❌ 无 | ✅ 逐节LaTeX (ICLR格式) + PDF编译 |
| **审查/改进** | ✅ 跨模型对抗审查 (最多4轮) + nightmare难度 | ❌ 仅val_bpb指标判断 | ✅ 可选LLM论文审查 | ⚠️ patience机制 (无改进则终止) | ✅ Judge Agent迭代修正 |

---

## 4. 工程能力对比

| 工程维度 | ARIS | autoresearch | AI-Scientist-v2 | Alchemy | AI-Researcher |
|---------|------|-------------|----------------|---------|--------------|
| **GPU支持** | 本地/远程/Vast.ai/Modal | 单GPU (H100) | 沙箱执行 | 多节点GPU调度 | Docker容器+GPU |
| **容器化** | ❌ 无 (依赖screen/SSH) | ❌ 无 | ⚠️ 沙箱Python | ✅ Docker/Singularity | ✅ Docker |
| **并发能力** | 队列调度 (40+任务) | 单任务顺序 | 并行Worker (可配置) | 最多32并发 | 顺序执行 |
| **通知系统** | ✅ 飞书(Lark)通知 | ❌ 无 | ❌ 无 | ❌ 无 | ❌ 无 (有Gradio UI) |
| **可视化** | matplotlib图表 | progress.png | 统一树可视化HTML | 实时终端Rich表格 | ❌ 无内置 |
| **可扩展性** | 高 (skill插件化) | 低 (固定单文件) | 中 (可配置模型/参数) | 中 (TaskPlugin抽象) | 中 (benchmark可扩展) |
| **Web界面** | ❌ 无 | ❌ 无 | ❌ 无 | ❌ 无 | ✅ Gradio Web UI |

---

## 5. 论文产出能力对比

| 论文维度 | ARIS | autoresearch | AI-Scientist-v2 | Alchemy | AI-Researcher |
|---------|------|-------------|----------------|---------|--------------|
| **论文生成** | ✅ 完整LaTeX | ❌ | ✅ 完整LaTeX+PDF | ❌ | ✅ 完整LaTeX+PDF |
| **会议格式** | ICLR/NeurIPS/ICML/CVPR/ACL/AAAI/IEEE等 | ❌ | ICBINB/ICML | ❌ | ICLR 2025 |
| **引用验证** | ✅ DBLP/CrossRef验证+引用审计 | ❌ | ✅ Semantic Scholar引用 | ❌ | ⚠️ 自动BibTeX (无验证) |
| **论文类型** | 实证/理论/方法/调研 | ❌ | 实验型 | ❌ | 实验型 |
| **图表生成** | ✅ 从数据自动生成 | ❌ 仅progress.png | ✅ VLM分析图表质量 | ❌ | ✅ 实验结果图表 |
| **写作质量审计** | ✅ 5轮审计 (Stanford写作课方法论) | ❌ | ❌ | ❌ | ⚠️ 最终checklist |

---

## 6. 核心差异化特征

### ARIS
- **跨模型对抗审查**：执行者与审查者必须是不同模型家族，nightmare难度下审查者直接读取源码，无法被过滤
- **飞书通知**：阶段切换时自动推送消息到移动端/桌面端
- **实验队列编排**：OOM重试、波次调度、阶段依赖、状态持久化
- **DBLP引用验证**：每条BibTeX引用都需在出版商数据库中验证，杜绝幻觉引用
- **理论论文支持**：完整证明导入、定理重述审计、先验边界对比表

### autoresearch
- **极致简洁**：仅4个核心文件，零学习成本
- **固定时间预算**：5分钟训练时间使所有实验直接可比
- **Git追踪**：只保留改进的提交，失败实验被reset，形成干净的改进轨迹
- **过夜运行**：~12实验/小时，一夜约100个实验

### AI-Scientist-v2
- **首个AI通过同行评审的论文**：已验证端到端自主科研的可行性
- **渐进式树搜索**：4阶段 (实现→调参→创新→消融)，每阶段自动推进
- **VLM图表分析**：视觉语言模型分析实验图表质量，提供改进反馈
- **模板无关创意生成**：v2不再依赖人工模板，LLM自主生成研究方向

### Alchemy
- **轨迹知识学习**：从实验历史中提取可复用的领域知识，跨任务积累
- **多温度多样性采样**：[0.3, 0.5, 0.7, 0.9] 四种温度探索不同假设空间
- **领域知识框架**：预存知识文件为LLM提供专业技术上下文
- **高并发**：最多32个实验同时运行，多节点GPU调度

### AI-Researcher
- **7+专用Agent协作**：Idea/Survey/Plan/ML/Judge/ExpAnalyser等Agent各司其职
- **浏览器环境**：BrowserGym + Playwright 实现真实网页浏览
- **Docker隔离**：容器化执行保证实验环境一致性
- **Judge Agent自修正**：迭代评估-修正循环直到实现正确
- **Gradio Web UI**：实时日志流、环境变量管理、产物下载

---

## 7. 适用场景推荐

| 你想做什么 | 最佳选择 | 理由 |
|-----------|---------|------|
| 快速上手，体验AI自主研究 | **autoresearch** | 4个文件，5分钟出结果，零配置 |
| 端到端产出可投稿论文 | **AI-Scientist-v2** 或 **ARIS** | 唯二支持完整论文生成+审查的项目 |
| 优化已有ML算法 | **Alchemy** | 种子基线+迭代优化，多温度探索 |
| 从零做科研 (含文献调研) | **ARIS** 或 **AI-Researcher** | 都有完整流程，ARIS文献源更丰富 |
| 大规模多GPU实验 | **ARIS** 或 **Alchemy** | ARIS有队列调度，Alchemy有32并发 |
| 学习AI研究Agent架构 | **autoresearch** 或 **AI-Researcher** | autoresearch极简，AI-Researcher展示多Agent模式 |
| 理论型论文 | **ARIS** | 唯一支持理论论文的项目 (证明导入、定理审计) |
| 算法优化竞赛 | **Alchemy** | 迭代优化+轨迹学习+高并发 |

---

## 8. 总结

这五个项目代表了AI自动化研究的不同哲学：

- **ARIS** 追求**完整性和严谨性**——从文献到论文的全流程，跨模型审查保证质量
- **autoresearch** 追求**极简和效率**——最小可行框架，一夜百次实验
- **AI-Scientist-v2** 追求**自主性和探索深度**——树搜索探索更大的解空间
- **Alchemy** 追求**优化和知识积累**——在已有基础上持续改进，积累可复用知识
- **AI-Researcher** 追求**多Agent协作**——专业分工，各Agent各司其职

选择取决于你的研究目标：需要完整论文选ARIS或AI-Scientist-v2，需要快速实验选autoresearch，需要算法优化选Alchemy，需要多Agent架构参考选AI-Researcher。
