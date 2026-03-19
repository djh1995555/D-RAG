# 技术选型文档

## 一、前端框架选择

### 主流前端框架对比

| 框架 | 语言 | 定位 | 输出平台 | AI 友好度 |
|------|------|------|----------|----------|
| **Next.js** | TypeScript | React 全栈框架 | Web / 移动端(TWA/PWA) | ⭐⭐⭐⭐⭐ |
| **Vue 3** | TypeScript | 渐进式前端框架 | Web / App(Weex) / 桌面端(Electron) | ⭐⭐⭐⭐ |
| **Nuxt** | TypeScript | Vue 全栈框架 | Web / 移动端(H5+PWA) | ⭐⭐⭐⭐⭐ |
| **React Native** | JavaScript | 原生 App | iOS/Android | ⭐⭐⭐ |

**结论**：
- AI 编程最友好 → **Next.js**（训练数据最多）
- 如果必须用 Vue → **Nuxt**（全栈）

---

## 二、后端框架选择

### 主流后端框架对比

| 框架 | 语言 | 优点 | 缺点 |
|------|------|------|------|
| **Next.js** | TypeScript | 全栈统一、部署简单、SSR/SEO | 冷启动慢、封装多 |
| **Nuxt** | TypeScript | Vue 亲儿子、全栈统一 | 生态不如 Next.js |
| **FastAPI** | Python | 性能高、自动文档、AI 生态 | 前后端分离、部署复杂 |
| **微信云开发** | JavaScript | 免费、微信生态无缝、免服务器 | 只能微信小程序用、查询能力弱 |
| **阿里云函数计算** | 多语言 | 按量付费、无需管理服务器、阿里云生态 | 需要自己搭建、配置复杂 |

**AI 编程最优解**：
- 前端 Vue → **Nuxt**
- 前端 React → **Next.js**
- 需要 Python AI 库 → **FastAPI**
- 微信小程序 → **微信云开发**
- 多端小程序 + 阿里云 → **阿里云函数计算**

---

## 三、数据库选择

### 方案对比

| 数据库 | 类型 | 费用 | 优点 | 适用场景 |
|--------|------|------|------|----------|
| **Supabase** | PostgreSQL | 免费 | 免费额度大、自带 API | 快速开发、个人项目 |
| **Neon** | PostgreSQL | 按量付费 | Serverless、分支功能 | Serverless 架构 |
| **Prisma** | ORM | 免费 | 类型安全、跨数据库 | 配合 Nuxt/Next.js |
| **微信云开发** | 文档数据库 | ¥0 起 | 免费、微信生态好 | 纯微信小程序 |
| **阿里云 RDS** | MySQL | ¥60+/月 | 国内快、备案方便 | 商业项目、国内上线 |

**推荐组合**：
- 个人/学习 → Supabase（免费够用）
- 微信小程序 → 微信云开发（免费）
- 商业项目 → 阿里云 RDS + Nuxt 后端

---
## 四、DCloud生态
| 部件 | 名称 | 介绍 |
|--------|------|------|
| 前端 | **uni-app** | TypeScript，跨端框架，可做小程序/H5/App
| 后端 | **uni-cloud** | 基于Node.js，配套uni-app，如果只需要简单功能，用云函数即可，复杂功能再开发后端
| 数据库 | **uni-cloud MongoDB** | MongoDB，阿里云免费套餐，云函数每月1.5万次，云数据库每日500RU| 

## 五、微信/多端小程序方案

### 方案对比

| 方案 | 输出平台 | 费用 | 难度 | 前端 | 后端 | 数据库 |
|------|----------|------|------|------|--------|--------|
| **微信云开发** | 微信小程序 | ¥0 起 | ⭐ | 微信语法WXML | 微信云开发 | 微信云数据库 |
| **uni-app + uni-cloud** | 多端小程序 + App + H5 | ¥0 起（免费）/ ¥5/月起 | ⭐⭐ | Vue | uni-cloud | uni-cloud MongoDB |
| **uni-app + 阿里云** | 多端小程序 + App + H5 | ¥60+/月 | ⭐⭐⭐ | Vue | 阿里云函数 | 阿里云 RDS |
| **Nuxt全栈** | H5（可在微信中打开） | ¥0 起 | ⭐⭐⭐ | Nuxt | Nuxt server | Supabase/Neon |

## 六、总结

| 需求 | 推荐技术栈 |
|------|-----------|
| 多端小程序（微信/支付宝/抖音）+ App | DCloud uni-app + uni-cloud |
| 纯微信小程序 + 省心 | 微信云开发 |
| Vue 全栈 + AI 友好 | Nuxt + Supabase |
| React 全栈 | Next.js + Supabase/Neon |
| Python AI 后端 | FastAPI + Vue/Nuxt 前端 |
| 个人学习 + 免费 | 微信云开发 或 Supabase |

