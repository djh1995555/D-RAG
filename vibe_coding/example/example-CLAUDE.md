# 项目名: Task Manager App

> 一个基于 React + Express + PostgreSQL 的全栈任务管理应用

## 项目概述

- **名称**: Task Manager
- **描述**: 支持用户注册、任务CRUD、任务分类、截止日期的任务管理系统
- **技术栈**:
  - 前端: React 18 + TypeScript + Tailwind CSS
  - 后端: Express.js + TypeScript
  - 数据库: PostgreSQL + Prisma ORM
  - 认证: JWT

## 项目结构

```
.
├── apps/
│   ├── web/                    # React 前端
│   │   ├── src/
│   │   │   ├── components/     # 可复用组件
│   │   │   ├── pages/          # 页面组件
│   │   │   ├── hooks/          # 自定义 hooks
│   │   │   ├── services/       # API 调用
│   │   │   └── types/          # TypeScript 类型
│   │   └── package.json
│   └── api/                    # Express 后端
│       ├── src/
│       │   ├── routes/         # API 路由
│       │   ├── controllers/    # 控制器
│       │   ├── services/       # 业务逻辑
│       │   ├── middleware/     # 中间件
│       │   ├── models/         # 数据模型
│       │   └── utils/          # 工具函数
│       └── package.json
├── packages/
│   └── shared/                 # 共享类型和工具
├── prisma/
│   └── schema.prisma           # 数据库 schema
├── docker-compose.yml          # 开发环境服务
└── package.json                # 根目录 workspace 配置
```

## 开发环境设置

### 前置要求
- Node.js 20+
- pnpm
- Docker & Docker Compose

### 首次启动

```bash
# 1. 安装依赖
pnpm install

# 2. 启动数据库（在后台运行）
docker-compose up -d postgres

# 3. 运行数据库迁移
pnpm db:migrate

# 4. 生成 Prisma Client
pnpm db:generate

# 5. 启动开发服务器（同时启动前后端）
pnpm dev
```

访问 http://localhost:5173 查看前端，API 运行在 http://localhost:3001

## 常用命令

| 命令 | 描述 |
|------|------|
| `pnpm dev` | 同时启动前端和后端开发服务器 |
| `pnpm dev:web` | 只启动前端 |
| `pnpm dev:api` | 只启动后端 |
| `pnpm db:migrate` | 运行数据库迁移 |
| `pnpm db:generate` | 生成 Prisma Client |
| `pnpm db:studio` | 打开 Prisma Studio 可视化数据库 |
| `pnpm db:seed` | 填充测试数据 |
| `pnpm build` | 构建生产版本 |
| `pnpm test` | 运行测试套件 |
| `pnpm lint` | 运行 ESLint 检查 |
| `pnpm lint:fix` | 自动修复 lint 问题 |

## 环境变量

### 前端 (apps/web/.env)
```bash
VITE_API_URL=http://localhost:3001/api
```

### 后端 (apps/api/.env)
```bash
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/taskmanager?schema=public"
JWT_SECRET=your-jwt-secret-key-change-in-production
PORT=3001
NODE_ENV=development
```

## 数据库 Schema

主要表结构：

- **User**: id, email, password, name, createdAt, updatedAt
- **Task**: id, title, description, status, priority, dueDate, userId, categoryId
- **Category**: id, name, color, userId

## API 端点

| 方法 | 端点 | 描述 |
|------|------|------|
| POST | /api/auth/register | 用户注册 |
| POST | /api/auth/login | 用户登录 |
| GET | /api/tasks | 获取当前用户的所有任务 |
| POST | /api/tasks | 创建新任务 |
| PUT | /api/tasks/:id | 更新任务 |
| DELETE | /api/tasks/:id | 删除任务 |
| GET | /api/categories | 获取分类列表 |

## 代码规范

### 命名规范
- 组件: PascalCase (e.g., `TaskCard.tsx`)
- Hooks: camelCase 前缀 use (e.g., `useAuth.ts`)
- 工具函数: camelCase (e.g., `formatDate.ts`)
- API 路由: kebab-case (e.g., `task-routes.ts`)
- 数据库模型: PascalCase 单数 (e.g., `User`, `Task`)

### 文件组织
- 按功能模块分组，而非按类型
- 组件放在其使用位置的最近处
- 共享类型放在 `packages/shared`

### 代码风格
- 使用 TypeScript 严格模式
- 优先使用函数组件和 hooks
- API 响应统一格式: `{ success: boolean, data?: T, error?: string }`

## 工作流偏好

- **提交**: 允许自动提交，但保持提交信息清晰
- **分支**: 使用 feature/ 前缀分支
- **沟通**: 对于较大的架构变更，先讨论再实施

## 测试

```bash
# 运行单元测试
pnpm test

# 运行 e2e 测试
pnpm test:e2e

# 测试覆盖率
pnpm test:coverage
```

## 部署

### 生产构建
```bash
pnpm build
```

### Docker 部署
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## 故障排除

### 数据库连接失败
- 确认 Docker 容器正在运行: `docker-compose ps`
- 检查 .env 中的 DATABASE_URL

### 类型错误
- 重新生成 Prisma Client: `pnpm db:generate`

### 端口被占用
- 检查 3001 或 5173 是否被占用
- 修改 .env 中的 PORT 或 VITE_PORT

## 相关链接

- [Prisma 文档](https://www.prisma.io/docs)
- [React 文档](https://react.dev)
- [Express 文档](https://expressjs.com)
