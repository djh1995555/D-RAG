[TOC]
# City Hunter (城市猎人) - 基于地理位置的城市解谜游戏
这是用原装的oh-my-opencode简单描述生成的任务文档，用来作为基准对比

## TL;DR

> **快速摘要**：在 6 周内构建一款基于地理位置的城市解谜小程序。Uni-app 跨平台前端 + Node.js 后端 + MongoDB。MVP：1 个城市，3-5 个案件，GPS 验证，以对话驱动的叙事方式提供线索，引导玩家前往真实世界地点。
> 
> **交付物**：
> - Uni-app 小程序（微信/支付宝/抖音）
> - Node.js 后端 + MongoDB 数据库
> - 内容管理后台
> - 3-5 个完整案件，包含 10-15 个真实世界地点
> - 支付集成（微信支付）
> - 测试覆盖率 ≥70%
> 
> **预估工作量**：大型（6 周，4 人全职团队）
> **并行执行**：是 - 5 个批次
> **关键路径**：基础架构 → 核心服务 → 前端集成 → 内容 → 部署

---

## 背景

### 原始需求
城市猎人是一款基于地理位置的城市解谜小程序。一级目录是城市,二级目录是案件,每个案件将会以对话的形式推进剧情,可以通过对话形式给出文字图片视频等,玩家需要在对话中获取线索,线索往往指向一个真实的城市地点。玩家去往该地点探索地标和文化景点,通过现场寻找线索来解开谜题,最终完成整个剧情。

### 访谈摘要
**关键讨论**：
- **平台**：Uni-app 实现跨平台（微信/支付宝/抖音）
- **地图服务**：腾讯地图 SDK，使用 gcj02 坐标系
- **后端**：Node.js + Express/Koa + MongoDB（游戏内容的灵活 Schema）
- **地点验证**：GPS 配合 50-100 米半径，GPS 失败时使用照片作为备选方案
- **功能**：MVP 核心（对话、线索、GPS 验证）+ 第二阶段（AR、UGC、排行榜）
- **商业模式**：付费下载（需要集成微信支付）
- **时间线**：调整为 6 周（1 个月紧凑开发 + 2 周缓冲）
- **测试策略**：TDD（测试驱动开发），目标覆盖率 70%

**研究发现**：
- **Ink Runtime**：生产就绪的对话引擎，支持分支叙事
- **XState Store**：事件驱动的状态管理，支持持久化
- **坐标系**：中国地图必须使用 gcj02（关键陷阱）
- **分包加载**：减少初始加载 40-60%（微信限制：主包 20MB + 分包各 16MB）
- **位置模拟**：用于测试的方法拦截模式，无需实地移动

### Metis 审查
**已识别的差距**（已解决）：
- **GPS 备选方案**：添加照片验证作为地下/室内场景的备选
- **支付集成**：添加微信支付商户账户设置任务
- **法律合规**：添加 ICP 备案和 PIPL 合规任务
- **范围控制**：第 1 周后冻结功能，设置明确的边界
- **边界情况**：添加地点关闭、GPS 失败、网络超时的处理

---

## 工作目标

### 核心目标
构建一款生产就绪的基于地理位置的解谜游戏小程序，具有对话驱动的叙事、真实世界地点探索和 GPS 验证功能。在 6 周内上线 1 个城市、3-5 个案件。

### 具体交付物
- **前端**：Uni-app 小程序（兼容微信/支付宝/抖音）
- **后端**：Node.js API 服务器 + MongoDB 数据库
- **管理后台**：案件/地点/线索的内容管理系统
- **内容**：3-5 个完整案件，10-15 个已验证的真实世界地点
- **测试**：Vitest（前端）+ Jest（后端），覆盖率 ≥70%
- **文档**：API 文档、部署指南、内容创作指南

### 完成定义
- [ ] 所有测试通过（bun test → 0 failures）
- [ ] 小程序通过微信/支付宝平台审核
- [ ] ICP 备案完成
- [ ] 支付流程端到端测试完成（沙盒 + 生产）
- [ ] 3-5 个案件内容审核并部署
- [ ] GPS 验证在 5 个以上真实地点测试
- [ ] 管理后台运行正常，内容编辑已培训

### 必须有
- 支持分支叙事的对话系统（Ink 启发的架构）
- GPS 地点验证，配合照片备选方案
- 线索发现和追踪系统
- 用户认证和云端同步
- 内容管理后台
- 支付集成（微信支付）
- 对话播放的离线支持
- TDD 开发，测试覆盖率 ≥70%

### 禁止事项（边界限制）
- 禁止配音（MVP 范围）
- 禁止动画角色肖像（仅静态图片）
- 禁止室内导航
- 禁止实时多人游戏
- 禁止社交功能（好友、分享、组队）- 第二阶段
- 禁止 AR 沉浸式叠加（MVP 仅支持图像识别触发）
- 禁止可视化内容编辑器（MVP 手动输入内容）
- 禁止每个对话节点分支深度 > 3 层

---

## 验证策略（强制执行）

> **零人工干预** — 所有验证由 agent 执行。无例外。
> 要求"用户手动测试/确认"的验收标准是禁止的。

### 测试决策
- **基础设施存在**：否（全新项目）
- **自动化测试**：是（TDD - 测试驱动开发）
- **前端框架**：Vitest + Vue Test Utils + @vue/vue3-jest
- **后端框架**：Jest + Supertest + mongodb-memory-server
- **E2E 框架**：Playwright（小程序开发者工具模式）
- **测试方法**：每个任务遵循 RED-GREEN-REFACTOR 循环

### QA 策略
每个任务必须包含 agent 执行的 QA 场景（见下方 TODO 模板）。
证据保存至 `.sisyphus/evidence/task-{N}-{scenario-slug}.{ext}`。

- **前端/UI**：使用 Playwright（playwright skill）— 导航小程序、与组件交互、断言 DOM、截图
- **API/后端**：使用 Bash（curl）— 向本地服务器发送请求、断言状态码和响应字段
- **位置服务**：使用模拟 GPS 坐标 + 照片上传模拟
- **数据库**：使用 mongodb-memory-server 进行隔离测试实例

---

## 执行策略

### 并行执行批次

> 通过将独立任务分组为并行批次来最大化吞吐量。
> 每个批次完成后才开始下一个。
> 目标：每批次 5-8 个任务。每批次少于 3 个（最后一批除外）= 分拆不足。

```
Wave 1 (Week 1 - Foundation & Scaffolding):
├── Task 1: Project initialization & repo setup [quick]
├── Task 2: Database schema design + Mongoose models [quick]
├── Task 3: Backend API structure + middleware [quick]
├── Task 4: Frontend project scaffold + routing [quick]
├── Task 5: Test framework setup (Vitest + Jest) [quick]
├── Task 6: Docker + docker-compose for dev environment [quick]
└── Task 7: CI/CD pipeline (GitHub Actions) [quick]

Wave 2 (Week 2 - Core Services):
├── Task 8: User authentication system (JWT + WeChat OAuth) [deep]
├── Task 9: Dialogue engine core (state machine + persistence) [deep]
├── Task 10: Location service (GPS verification + Tencent Map API) [unspecified-high]
├── Task 11: Clue system (discovery + tracking + relationships) [unspecified-high]
├── Task 12: File storage service (OSS + image processing) [quick]
└── Task 13: Error tracking + logging infrastructure [quick]

Wave 3 (Week 3-4 - Frontend Development):
├── Task 14: City selection UI + case list UI [visual-engineering]
├── Task 15: Dialogue player component [visual-engineering]
├── Task 16: Clue inventory UI [visual-engineering]
├── Task 17: Map exploration UI (Tencent Map integration) [visual-engineering]
├── Task 18: Location verification UI (GPS + camera) [visual-engineering]
├── Task 19: User profile + progress tracking UI [visual-engineering]
├── Task 20: State management (Pinia stores) [quick]
└── Task 21: Offline support (local storage + sync queue) [unspecified-high]

Wave 4 (Week 5 - Content & Admin):
├── Task 22: Admin panel - case management [visual-engineering]
├── Task 23: Admin panel - location management [visual-engineering]
├── Task 24: Admin panel - clue management [visual-engineering]
├── Task 25: Content creation tools (dialogue editor) [unspecified-high]
├── Task 26: Sample case content creation (Case 1) [writing]
├── Task 27: Sample case content creation (Case 2) [writing]
└── Task 28: Sample case content creation (Case 3) [writing]

Wave 5 (Week 6 - Integration & Deployment):
├── Task 29: Payment integration (WeChat Pay) [deep]
├── Task 30: Mini-program platform submission & review [unspecified-high]
├── Task 31: ICP filing & compliance documentation [writing]
├── Task 32: Performance optimization (bundle size, lazy loading) [quick]
├── Task 33: Production deployment (backend + database + CDN) [quick]
└── Task 34: Monitoring & alerting setup [quick]

Wave FINAL (After ALL tasks - independent review, 4 parallel):
├── Task F1: Plan compliance audit (oracle)
├── Task F2: Code quality review (unspecified-high)
├── Task F3: Real location testing QA (unspecified-high)
└── Task F4: Scope fidelity check (deep)

Critical Path: Task 1 → Task 2 → Task 8 → Task 9 → Task 15 → Task 22 → Task 29 → Task 30 → F1-F4
Parallel Speedup: ~65% faster than sequential
Max Concurrent: 8 (Wave 1)
```

### 依赖矩阵（简版 — 在生成的计划中显示所有任务）

- **1-7**: — — 8-13, 1
- **8**: 1-7 — 9-11, 14-19, 20, 22-28, 29, 2
- **9**: 1-7, 8 — 15, 16, 25, 3
- **10**: 1-7 — 17, 18, 24, 4
- **11**: 1-7 — 16, 24, 5
- **12**: 1-7 — 18, 22-24, 26-28, 6
- **13**: 1-7 — F2, 7
- **14-21**: 8-11, 20 — 22-28, F3, 8
- **22-28**: 8-13, 20-21 — 29-34, F1, 9
- **29-34**: 22-28 — F1-F4, 10
- **F1-F4**: 1-34 — —

> 这是简版参考。你生成的计划必须包含所有任务的完整矩阵。

### Agent 调度摘要

- **1**: **7** — T1-T4 → `quick`, T5-T7 → `quick`
- **2**: **6** — T8 → `deep`, T9 → `deep`, T10-T11 → `unspecified-high`, T12-T13 → `quick`
- **3**: **8** — T14-T19 → `visual-engineering`, T20 → `quick`, T21 → `unspecified-high`
- **4**: **7** — T22-T24 → `visual-engineering`, T25 → `unspecified-high`, T26-T28 → `writing`
- **5**: **6** — T29 → `deep`, T30-T31 → `unspecified-high`/`writing`, T32-T34 → `quick`
- **FINAL**: **4** — F1 → `oracle`, F2 → `unspecified-high`, F3 → `unspecified-high`, F4 → `deep`

---

## TODOs

> 实现 + 测试 = 一个任务。永不分离。
> 每个任务必须包含：推荐的 Agent Profile + 并行化信息 + QA 场景。
> **没有 QA 场景的任务是不完整的。无例外。**

### Wave 1: 基础架构与脚手架（第 1 周）

- [x] 1. 项目初始化与仓库设置 [quick] ✅

  **做什么**：初始化 Uni-app（Vue 3 + TS）+ Node.js（Express + TS）monorepo，设置 ESLint/Prettier，git 分支（main/develop），README.md
  
  **禁止事项**：安装完整的 UI 组件库、不必要的依赖
  
  **参考**：Uni-app CLI 文档，Express TypeScript 入门模板
  
  **验收标准**: 
  - [ ] Test passes: "project initialized"
  - [ ] Git clean working tree
  - [ ] Both frontend/backend TypeScript compile successfully
  
  **QA 场景**:
  ```bash
  # Scenario: Structure validation
  ls -la frontend/ backend/ shared/  # All exist
  git branch -a  # main/develop exist
  npm run lint  # No errors
  ```
  **证据**: .sisyphus/evidence/task-01-*.txt
  
  **提交**: `chore: initialize monorepo with uni-app + express`

- [x] 2. 数据库 Schema 设计 + Mongoose 模型 [quick] ✅

  **做什么**：设计 MongoDB schemas（User, Case, Clue, Location, Progress, DialogueSnapshot），创建带有 TS 接口的 Mongoose 模型，添加验证，种子数据脚本
  
  **禁止事项**：过度设计关系、添加不必要的索引
  
  **参考**：Mongoose TypeScript 文档，研究中发现的 Ink 状态模式
  
  **验收标准**:
  - [ ] Schema validation tests pass
  - [ ] Seed data creates ≥1 user, ≥1 case
  
  **QA 场景**:
  ```bash
  npm run test:models  # All schemas valid
  npm run seed:dev && mongosh -e "db.users.countDocuments()"  # ≥1
  ```
  **证据**: .sisyphus/evidence/task-02-*.txt
  
  **提交**: `feat(db): add mongoose schemas and models`

- [x] 3. 后端 API 结构 + 中间件 [quick] ✅

  **做什么**：设置 Express 应用，创建中间件（errorHandler, cors, helmet, requestLogger），设置路由（/api/v1/auth, /cases, /locations），添加请求验证（Zod）
  
  **禁止事项**：实现业务逻辑，暂不添加认证中间件
  
  **验收标准**:
  - [ ] Health endpoint returns 200 OK
  - [ ] 404 handled gracefully
  
  **QA 场景**:
  ```bash
  curl localhost:3000/api/v1/health  # {"status":"ok"}
  curl localhost:3000/api/v1/nonexistent  # 404
  ```
  **证据**: .sisyphus/evidence/task-03-*.txt
  
  **提交**: `feat(api): setup express structure and middleware`

- [x] 4. 前端项目脚手架 + 路由 [quick] ✅

  **做什么**：设置 Uni-app 页面（city-list, case-list, dialogue, map, profile），配置路由，创建页面布局，添加导航守卫
  
  **禁止事项**：暂不构建完整的 UI 组件
  
  **验收标准**:
  - [ ] All pages render without errors
  - [ ] Navigation between pages works
  
  **QA 场景**:
  ```bash
  # Use Playwright mini-program devtools
  page.goto('pages/city-list/index')  # Renders
  page.click('[data-test="case-item"]')  # Navigates to case-list
  ```
  **证据**: .sisyphus/evidence/task-04-*.png
  
  **提交**: `feat(frontend): setup pages and routing`

- [x] 5. 测试框架设置（Vitest + Jest）[quick] ✅

  **做什么**：配置前端 Vitest（Vue Test Utils），后端 Jest（Supertest, mongodb-memory-server），添加覆盖率脚本，创建测试工具
  
  **验收标准**:
  - [ ] `bun test` runs all tests
  - [ ] Coverage report generated
  
  **QA 场景**:
  ```bash
  cd frontend && npm test  # Vitest runs
  cd backend && npm test  # Jest runs
  npm run coverage  # Report generated
  ```
  **证据**: .sisyphus/evidence/task-05-coverage.html
  
  **提交**: `test: setup vitest and jest frameworks`

- [x] 6. Docker + Docker Compose 开发环境 [quick] ✅

  **做什么**：创建前端/后端的 Dockerfile，docker-compose.yml（MongoDB, Redis, MinIO），.dockerignore，开发脚本
  
  **验收标准**:
  - [ ] `docker-compose up` starts all services
  - [ ] Backend connects to MongoDB in container
  
  **QA 场景**:
  ```bash
  docker-compose up -d
  docker ps  # 3 containers running
  curl localhost:3000/api/v1/health  # OK
  ```
  **证据**: .sisyphus/evidence/task-06-docker.txt
  
  **提交**: `feat(devops): add docker configuration`

- [x] 7. CI/CD 流水线（GitHub Actions）[quick] ✅

  **做什么**：创建 .github/workflows/ci.yml（lint, test, build），cd.yml（部署到 staging/prod），添加 secrets 文档
  
  **验收标准**:
  - [ ] CI runs on PR
  - [ ] All checks pass on develop branch
  
  **QA 场景**:
  ```bash
  # Simulate CI locally
  act pull_request  # If act installed
  # Or verify on GitHub PR
  ```
  **证据**: .sisyphus/evidence/task-07-ci-screenshot.png
  
  **提交**: `ci: add github actions workflows`

### Wave 2: 核心服务（第 2 周）

- [x] 8. 用户认证系统（JWT + 微信 OAuth）[deep] ✅

  **做什么**：实现 JWT 认证，微信小程序 OAuth 流程，用户注册/登录端点，token 刷新，密码哈希（bcrypt）
  
  **禁止事项**：明文存储密码，跳过 token 过期设置
  
  **参考**：微信小程序登录文档，JWT 最佳实践
  
  **验收标准**:
  - [ ] User can register/login via WeChat OAuth
  - [ ] JWT token issued and validated
  - [ ] Token refresh works
  
  **QA 场景**:
  ```bash
  # Mock WeChat OAuth
  curl -X POST localhost:3000/api/v1/auth/wechat -d '{"code":"test_code"}'
  # Returns {token, user}

  curl -H "Authorization: Bearer $TOKEN" localhost:3000/api/v1/auth/me
  # Returns user profile
  ```
  **证据**: .sisyphus/evidence/task-08-auth-flow.txt
  
  **提交**: `feat(auth): implement JWT and WeChat OAuth`

- [x] 9. 对话引擎核心（状态机 + 持久化）[deep] ✅

  **做什么**：实现对话状态机（XState 启发），对话节点渲染，选项选择，变量追踪，保存/加载状态，对话历史
  
  **禁止事项**：添加配音、动画肖像
  
  **参考**：Ink runtime 架构，研究中发现的 XState 模式
  
  **验收标准**:
  - [ ] Dialogue progresses through nodes
  - [ ] Choices navigate to correct nodes
  - [ ] State saves/loads correctly
  
  **QA 场景**:
  ```bash
  # API test
  curl -X POST localhost:3000/api/v1/dialogue/start -d '{"caseId":"case1"}'
  # Returns first dialogue node

  curl -X POST localhost:3000/api/v1/dialogue/choice -d '{"choiceIndex":0}'
  # Returns next node
  ```
  **证据**: .sisyphus/evidence/task-09-dialogue-flow.txt
  
  **提交**: `feat(dialogue): implement dialogue engine core`

- [x] 10. 地点服务（GPS 验证 + 腾讯地图 API）[unspecified-high] ✅

  **做什么**：实现 GPS 坐标验证（Haversine 距离计算），腾讯地图 API 集成（地理编码、POI 搜索），地点缓存，照片验证备选方案
  
  **禁止事项**：使用 WGS-84 坐标（必须使用 gcj02）
  
  **参考**：腾讯 LBS SDK，研究中发现的坐标转换
  
  **验收标准**:
  - [ ] GPS coordinates verified within 100m
  - [ ] Tencent Map POI search works
  - [ ] Photo fallback triggers when GPS fails
  
  **QA 场景**:
  ```bash
  # Mock GPS
  curl -X POST localhost:3000/api/v1/location/verify \
    -d '{"lat":39.9042,"lng":116.4074,"targetLocationId":"loc1"}'
  # Returns {verified: true, distance: 50}

  # GPS fail scenario
  curl -X POST localhost:3000/api/v1/location/verify \
    -d '{"lat":0,"lng":0,"targetLocationId":"loc1","fallback":"photo"}'
  # Returns {verified: false, requiresPhoto: true}
  ```
  **证据**: .sisyphus/evidence/task-10-location-verify.txt
  
  **提交**: `feat(location): implement GPS verification and Tencent Map integration`

- [x] 11. 线索系统（发现 + 追踪 + 关联）[unspecified-high] ✅

  **做什么**：实现线索发现（从对话/地点），线索库存，线索关联（线索之间的连接），线索与谜题的关联
  
  **验收标准**:
  - [ ] Clues discovered from dialogue choices
  - [ ] Clues discovered from location visits
  - [ ] Clue relationships tracked
  
  **QA 场景**:
  ```bash
  curl -X POST localhost:3000/api/v1/clues/discover \
    -d '{"clueId":"clue1","source":"dialogue","nodeId":"node5"}'
  # Returns clue details

  curl localhost:3000/api/v1/clues/inventory
  # Returns all discovered clues
  ```
  **证据**: .sisyphus/evidence/task-11-clue-system.txt
  
  **提交**: `feat(clues): implement clue discovery and tracking`

- [x] 12. 文件存储服务（OSS + 图像处理）[quick] ✅

  **做什么**：集成阿里云 OSS（或腾讯 COS），图片上传/处理（sharp），文件验证，CDN 配置
  
  **验收标准**:
  - [ ] Files upload to OSS successfully
  - [ ] Images resized/optimized
  - [ ] CDN URLs generated
  
  **QA 场景**:
  ```bash
  curl -X POST localhost:3000/api/v1/upload \
    -F "file=@test.jpg"
  # Returns {url: "https://cdn.../test.jpg"}
  ```
  **证据**: .sisyphus/evidence/task-12-file-upload.txt
  
  **提交**: `feat(storage): add OSS file storage service`

- [x] 13. 错误追踪 + 日志基础设施 [quick] ✅

  **做什么**：集成 Sentry 用于错误追踪，Winston 用于日志记录，结构化日志格式，日志聚合设置
  
  **验收标准**:
  - [ ] Errors reported to Sentry
  - [ ] Logs written to file/console
  - [ ] Structured JSON log format
  
  **QA 场景**:
  ```bash
  # Trigger error
  curl localhost:3000/api/v1/error-test
  # Check Sentry dashboard for error report
  tail -f logs/combined.log  # Structured JSON
  ```
  **证据**: .sisyphus/evidence/task-13-error-tracking.txt
  
  **提交**: `feat(logging): add Sentry and Winston logging`

### Wave 3: 前端开发（第 3-4 周）

- [x] 14. 城市选择 UI + 案件列表 UI [visual-engineering] ✅

  **做什么**：构建城市选择界面（网格/列表视图），案件列表界面（按城市筛选），带有预览的案件卡片，锁定/解锁状态
  
  **参考**：研究中的 UI 模式，微信设计指南
  
  **验收标准**:
  - [ ] Cities displayed in grid
  - [ ] Cases filtered by selected city
  - [ ] Locked cases show payment prompt
  
  **QA 场景**:
  ```javascript
  // Playwright test
  await page.goto('pages/city-list/index')
  await expect(page.locator('.city-card')).toHaveCount(3)
  await page.click('.city-card:first-child')
  await expect(page).toHaveURL(/case-list/)
  await expect(page.locator('.case-card.unlocked')).toHaveCount(2)
  ```
  **证据**: .sisyphus/evidence/task-14-city-case-ui.png
  
  **提交**: `feat(ui): add city and case selection screens`

- [x] 15. 对话播放器组件 [visual-engineering] ✅

  **做什么**：构建对话气泡组件，选项按钮，说话者肖像，对话历史滚动，文字动画效果
  
  **禁止事项**：添加配音、动画肖像（仅静态图片）
  
  **参考**：研究中的 Ink/视觉小说模式
  
  **验收标准**:
  - [ ] Dialogue text displays with typing effect
  - [ ] Choices appear when available
  - [ ] History scrollable
  
  **QA 场景**:
  ```javascript
  await page.goto('pages/dialogue/index?caseId=case1')
  await expect(page.locator('.dialogue-bubble')).toBeVisible()
  await page.click('.choice-button:first-child')
  await expect(page.locator('.dialogue-bubble')).toContainText('...')
  ```
  **证据**: .sisyphus/evidence/task-15-dialogue-player.png
  
  **提交**: `feat(ui): implement dialogue player component`

- [x] 16. 线索库存 UI [visual-engineering] ✅

  **做什么**：构建线索库存界面，带有详情的线索卡片，线索关联可视化，线索筛选/搜索
  
  **验收标准**:
  - [ ] Discovered clues displayed in grid
  - [ ] Clue details viewable
  - [ ] Related clues linked
  
  **QA 场景**:
  ```javascript
  await page.goto('pages/inventory/index')
  await expect(page.locator('.clue-card')).toHaveCount(5)
  await page.click('.clue-card:first-child')
  await expect(page.locator('.clue-detail')).toBeVisible()
  ```
  **证据**: .sisyphus/evidence/task-16-clue-inventory.png
  
  **提交**: `feat(ui): add clue inventory screen`

- [x] 17. 地图探索 UI（腾讯地图集成）[visual-engineering] ✅

  **做什么**：集成腾讯地图组件，绘制地点标记，显示当前位置，地点详情弹窗，导航提示
  
  **禁止事项**：室内导航、实时位置共享
  
  **参考**：腾讯地图小程序 SDK 文档
  
  **验收标准**:
  - [ ] Map displays with location markers
  - [ ] Current location shown
  - [ ] Marker tap shows location details
  
  **QA 场景**:
  ```javascript
  await page.goto('pages/map/index?caseId=case1')
  await expect(page.locator('map')).toBeVisible()
  await page.click('.location-marker:first-child')
  await expect(page.locator('.location-popup')).toBeVisible()
  ```
  **证据**: .sisyphus/evidence/task-17-map-ui.png
  
  **提交**: `feat(ui): integrate Tencent Map for exploration`

- [x] 18. 地点验证 UI（GPS + 相机）[visual-engineering] ✅

  **做什么**：构建 GPS 验证界面，相机捕获用于照片备选，验证成功/失败状态，距离指示器
  
  **验收标准**:
  - [ ] GPS verification shows distance to target
  - [ ] Camera capture for photo fallback
  - [ ] Success/failure feedback
  
  **QA 场景**:
  ```javascript
  // Mock GPS location
  await page.goto('pages/verify/index?locationId=loc1')
  await page.evaluate(() => {
    // Mock wx.getLocation to return target coordinates
    wx.getLocation = (opts) => opts.success({latitude: 39.9042, longitude: 116.4074})
  })
  await page.click('.verify-button')
  await expect(page.locator('.success-message')).toBeVisible()
  ```
  **证据**: .sisyphus/evidence/task-18-location-verify.png
  
  **提交**: `feat(ui): add location verification interface`

- [x] 19. 用户资料 + 进度追踪 UI [visual-engineering] ✅

  **做什么**：构建用户资料界面，进度指示器（已完成的案件、已访问的地点），成就徽章，设置
  
  **验收标准**:
  - [ ] User info displayed
  - [ ] Progress bars for cases/locations
  - [ ] Achievement badges shown
  
  **QA 场景**:
  ```javascript
  await page.goto('pages/profile/index')
  await expect(page.locator('.progress-bar')).toBeVisible()
  await expect(page.locator('.achievement-badge')).toHaveCount(3)
  ```
  **证据**: .sisyphus/evidence/task-19-profile-ui.png
  
  **提交**: `feat(ui): add user profile and progress tracking`

- [x] 20. 状态管理（Pinia Stores）[quick] ✅

  **做什么**：设置 Pinia stores（user, case, dialogue, clue, location），实现 actions/getters，添加持久化插件，与后端同步
  
  **验收标准**:
  - [ ] All state in Pinia stores
  - [ ] State persists across page reloads
  - [ ] Syncs with backend on login
  
  **QA 场景**:
  ```javascript
  // Test state persistence
  await page.goto('pages/dialogue/index')
  await page.click('.choice-button')
  await page.reload()
  await expect(page.locator('.dialogue-bubble')).toContainText('...')
  ```
  **证据**: .sisyphus/evidence/task-20-state-mgmt.txt
  
  **提交**: `feat(state): setup Pinia stores`

- [x] 21. 离线支持（本地存储 + 同步队列）[unspecified-high] ✅

  **做什么**：实现操作的离线队列，对话/线索的本地存储，在线时的后台同步，冲突解决
  
  **验收标准**:
  - [ ] Dialogue playable offline
  - [ ] Actions queued when offline
  - [ ] Auto-sync when reconnected
  
  **QA 场景**:
  ```javascript
  // Test offline mode
  await page.context().setOffline(true)
  await page.goto('pages/dialogue/index')
  await page.click('.choice-button')  // Queued
  await page.context().setOffline(false)
  await page.waitForTimeout(2000)
  // Check backend received queued action
  ```
  **证据**: .sisyphus/evidence/task-21-offline-sync.txt
  
  **提交**: `feat(offline): add offline support and sync queue`

### Wave 4: 内容与管理（第 5 周）

- [ ] 22-24. 管理后台（案件/地点/线索管理）[visual-engineering]

  **做什么**：构建管理后台，支持案件、地点、线索的 CRUD；对话编辑器（JSON/YAML），地图上的地点选择器，图片上传
  
  **验收标准**:
  - [ ] Admin can create/edit/delete cases
  - [ ] Location picker on map
  - [ ] Dialogue editor with validation
  
  **QA 场景**:
  ```javascript
  await page.goto('admin/cases')
  await page.click('.create-case')
  await page.fill('#title', 'New Case')
  await page.click('.save-button')
  await expect(page.locator('.case-card')).toContainText('New Case')
  ```
  **证据**: .sisyphus/evidence/task-22-24-admin-panel.png
  
  **提交**: `feat(admin): add content management panel`

- [ ] 25. 内容创作工具（对话编辑器）[unspecified-high]

  **做什么**：构建可视化对话编辑器（基于节点的图形），对话预览，导入/导出 JSON，验证
  
  **验收标准**:
  - [ ] Drag-and-drop dialogue nodes
  - [ ] Preview dialogue flow
  - [ ] Export to game format
  
  **QA 场景**:
  ```javascript
  await page.goto('admin/dialogue-editor')
  await page.dragAndDrop('.node-template', '.canvas')
  await page.click('.connect-nodes')
  await page.click('.preview-button')
  await expect(page.locator('.preview-dialogue')).toBeVisible()
  ```
  **证据**: .sisyphus/evidence/task-25-dialogue-editor.png
  
  **提交**: `feat(admin): add visual dialogue editor`

- [ ] 26-28. 示例案件内容创作（案件 1-3）[writing]

  **做什么**：编写 3 个完整案件的故事线、对话树、线索、地点；测试谜题可解性
  
  **验收标准**:
  - [ ] Each case has 30+ dialogue nodes
  - [ ] Each case has 3-5 locations
  - [ ] Puzzles tested and solvable
  
  **QA 场景**:
  ```bash
  # Content validation
  npm run validate:content
  # Verify case structure
  mongosh -e "db.cases.findOne({id: 'case1'}).dialogueNodes.length"  # ≥30
  ```
  **证据**: .sisyphus/evidence/task-26-28-content-creation.txt
  
  **提交**: `content: add sample cases 1-3`

### Wave 5: 集成与部署（第 6 周）

- [ ] 29. 支付集成（微信支付）[deep]

  **做什么**：集成微信支付 SDK，支付流程（订单创建 → 支付 → 验证），支付沙盒测试，退款处理
  
  **验收标准**:
  - [ ] Payment creates order
  - [ ] Payment verified
  - [ ] Case unlocked after payment
  
  **QA 场景**:
  ```javascript
  await page.goto('pages/case-detail/index?id=case2')
  await page.click('.unlock-button')
  // Mock WeChat Pay success
  await page.evaluate(() => {
    wx.requestPayment = (opts) => opts.success({})
  })
  await page.click('.confirm-payment')
  await expect(page.locator('.unlocked-message')).toBeVisible()
  ```
  **证据**: .sisyphus/evidence/task-29-payment-flow.txt
  
  **提交**: `feat(payment): integrate WeChat Pay`

- [ ] 30. 小程序平台提交与审核 [unspecified-high]

  **做什么**：准备提交材料，提交到微信/支付宝/抖音平台，处理审核反馈，获得批准
  
  **验收标准**:
  - [ ] Submitted to all 3 platforms
  - [ ] Approval received from at least 1 platform
  
  **QA 场景**:
  ```bash
  # Verify submission status
  # WeChat: mp.weixin.qq.com
  # Alipay: open.alipay.com
  # Douyin: microapp.bytedance.com
  ```
  **证据**: .sisyphus/evidence/task-30-platform-approval.png
  
  **提交**: `docs: add platform submission docs`

- [ ] 31. ICP 备案与合规文档 [writing]

  **做什么**：完成 ICP 备案申请，准备隐私政策、用户协议、PIPL 合规文档
  
  **验收标准**:
  - [ ] ICP filing submitted
  - [ ] Privacy policy published
  - [ ] PIPL compliance documented
  
  **QA 场景**:
  ```bash
  # Verify ICP number in footer
  curl https://yourdomain.com | grep "ICP"
  ```
  **证据**: .sisyphus/evidence/task-31-icp-compliance.txt
  
  **提交**: `docs: add ICP filing and compliance docs`

- [ ] 32. 性能优化（包大小、懒加载）[quick]

  **做什么**：优化包大小（总计 <15MB），实现懒加载，图片压缩，分包优化
  
  **验收标准**:
  - [ ] Main package <15MB
  - [ ] First screen load <3s
  - [ ] Images compressed
  
  **QA 场景**:
  ```bash
  npm run build
  du -sh dist/build/mp-weixin  # <15MB
  # Test first screen load time in WeChat DevTools
  ```
  **证据**: .sisyphus/evidence/task-32-performance.txt
  
  **提交**: `perf: optimize bundle size and lazy loading`

- [ ] 33. 生产环境部署（后端 + 数据库 + CDN）[quick]

  **做什么**：部署后端到云端（腾讯云/阿里云），设置 MongoDB Atlas 或自托管，配置 CDN，设置域名，SSL 证书
  
  **验收标准**:
  - [ ] Backend accessible via HTTPS
  - [ ] Database connected
  - [ ] CDN serving static assets
  
  **QA 场景**:
  ```bash
  curl https://api.yourdomain.com/health  # 200 OK
  curl https://cdn.yourdomain.com/test.jpg  # 200 OK
  ```
  **证据**: .sisyphus/evidence/task-33-deployment.txt
  
  **提交**: `deploy: production deployment`

- [ ] 34. 监控与告警设置 [quick]

  **做什么**：设置应用监控（Sentry 性能），数据库监控，告警规则，状态页面
  
  **验收标准**:
  - [ ] Metrics dashboard active
  - [ ] Alerts configured
  - [ ] Status page published
  
  **QA 场景**:
  ```bash
  # Trigger test alert
  curl https://api.yourdomain.com/test-error
  # Verify alert received
  ```
  **证据**: .sisyphus/evidence/task-34-monitoring.png
  
  **提交**: `ops: add monitoring and alerting`

---

## 最终验证批次（强制执行 — 在所有实现任务完成后）

> 4 个审查 agent 并行运行。全部必须通过。拒绝 → 修复 → 重新运行。

- [ ] F1. **计划合规性审计** — `oracle`
  
  **做什么**：完整阅读计划。对于每个"必须有"：验证实现存在（读取文件、curl 端点、运行命令）。对于每个"禁止事项"：搜索代码库中的禁止模式 — 如果发现则拒绝并指出 file:line。检查 .sisyphus/evidence/ 中的证据文件是否存在。将交付物与计划进行对比。
  
  **验证清单**:
  - [ ] All "Must Have" features implemented
  - [ ] All "Must NOT Have" features absent
  - [ ] All evidence files present
  - [ ] All tasks completed
  
  **输出**: `Must Have [N/N] | Must NOT Have [N/N] | Tasks [N/N] | VERDICT: APPROVE/REJECT`

- [ ] F2. **代码质量审查** — `unspecified-high`
  
  **做什么**：运行 `tsc --noEmit` + linter + `bun test`。审查所有修改文件：`as any`/`@ts-ignore`，空 catch，生产代码中的 console.log，注释掉的代码，未使用的导入。检查 AI slop：过多注释、过度抽象、通用名称（data/result/item/temp）。
  
  **验证命令**:
  ```bash
  cd frontend && npm run type-check && npm run lint
  cd backend && npm run type-check && npm run lint
  npm test -- --coverage
  ```
  
  **输出**: `Build [PASS/FAIL] | Lint [PASS/FAIL] | Tests [N pass/N fail] | Files [N clean/N issues] | VERDICT`

- [ ] F3. **真实地点测试 QA** — `unspecified-high`（+ `playwright` skill）
  
  **做什么**：从干净状态开始。执行每个任务的每个 QA 场景 — 遵循确切步骤，捕获证据。测试跨任务集成（功能协同工作，而非隔离）。测试边界情况：空状态、无效输入、快速操作。保存到 `.sisyphus/evidence/final-qa/`。
  
  **测试计划**:
  - [ ] All Wave 1-5 QA scenarios executed
  - [ ] Integration tests (login → play case → pay → unlock)
  - [ ] Edge cases tested (GPS fail, network offline, storage full)
  
  **输出**: `Scenarios [N/N pass] | Integration [N/N] | Edge Cases [N tested] | VERDICT`

- [ ] F4. **范围一致性检查** — `deep`
  
  **做什么**：对于每个任务：阅读"做什么"，阅读实际 diff（git log/diff）。验证 1:1 — 规格中的所有内容都已构建（无遗漏），没有构建规格之外的内容（无蔓延）。检查"禁止事项"合规性。检测跨任务污染：任务 N 修改了任务 M 的文件。标记未说明的更改。
  
  **验证流程**:
  ```bash
  git log --oneline --all
  git diff main..develop --stat
  # For each commit, verify it matches task spec
  ```
  
  **输出**: `Tasks [N/N compliant] | Contamination [CLEAN/N issues] | Unaccounted [CLEAN/N files] | VERDICT`

---

## 提交策略

- **原子提交**：一个任务 = 一个提交（或分组的逻辑单元）
- **提交格式**：`<type>(<scope>): <description>`
- **Pre-commit Hooks**：提交时运行 lint + test
- **分支策略**: 
  - `main` - 生产环境
  - `develop` - 集成环境
  - `feature/task-N-description` - 单个任务

**示例提交**:
```
chore: initialize monorepo with uni-app + express
feat(db): add mongoose schemas and models
feat(api): setup express structure and middleware
feat(auth): implement JWT and WeChat OAuth
feat(dialogue): implement dialogue engine core
feat(ui): add city and case selection screens
```

---

## 成功标准

### 验证命令
```bash
# Backend health
curl https://api.yourdomain.com/health
# Expected: {"status":"ok"}

# Database connection
mongosh "mongodb://localhost:27017/city-hunter" -e "db.stats()"
# Expected: {"ok":1}

# Test coverage
npm run coverage
# Expected: ≥70% coverage

# Mini-program build
cd frontend && npm run build:mp-weixin
# Expected: dist/build/mp-weixin/ <15MB

# Platform approval
# Expected: Approved on at least 1 platform (WeChat/Alipay/Douyin)
```

### 最终检查清单
- [ ] 所有"必须有"功能已实现
- [ ] 所有"禁止事项"未出现
- [ ] 所有测试通过（bun test → 0 failures）
- [ ] 测试覆盖率 ≥70%
- [ ] 小程序通过平台审核
- [ ] ICP 备案完成
- [ ] 支付流程端到端测试完成
- [ ] 3-5 个案件已部署
- [ ] GPS 验证在 5 个以上真实地点测试
- [ ] 管理后台运行正常
- [ ] 所有证据文件存在
- [ ] 所有最终验证任务通过

---

## 风险缓解

### 高风险项目
1. **GPS 精度**：在实际地点测试，准备好照片备选方案
2. **平台审核**：提前提交（第 4 周），准备备用平台
3. **支付集成**：在沙盒环境充分测试，准备好微信支付商户账户
4. **内容创作**：最晚第 5 周开始，必要时准备备用作者
5. **ICP 备案**：第 1 周开始（需要 2-4 周），准备好文档

### 应急计划
- **如果时间推迟**：减少到 3 个案件而非 5 个
- **如果 GPS 不可靠**：增加照片验证的使用
- **如果平台被拒**：优先通过已批准的平台，稍后提交其他平台
- **如果内容延迟**：使用占位内容，先上线 1 个案件

---

## 备注

- **坐标系**：中国地图始终使用 gcj02（而非 WGS-84）
- **小程序限制**：主包 ≤20MB，每个分包 ≤16MB
- **测试策略**：TDD 意味着先写测试，再实现
- **离线优先**：对话必须能在无网络情况下工作
- **安全**：所有地点必须经过公共可达性审查
