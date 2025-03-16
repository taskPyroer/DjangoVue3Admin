
# PaoDjangoAdmin

## 项目简介

PaoDjangoAdmin 是一个基于 Django + Vue3 的前后端分离的后台管理系统，采用了最新的前后端技术栈，内置了丰富的功能模块，可以帮助开发者快速搭建企业级中后台产品。

## 技术架构

### 后端技术栈

- **核心框架**：Django 4.2.1
- **权限认证**：Django REST framework + JWT + Casbin
- **数据库**：MySQL 8.0+
- **缓存**：Redis
- **任务队列**：Celery
- **WebSocket**：Channels + Redis
- **跨域处理**：django-cors-headers
- **验证码**：django-simple-captcha
- **数据导出**：django-import-export

### 前端技术栈

- **核心框架**：Vue 3.0 (Composition API)
- **开发语言**：TypeScript
- **构建工具**：Vite 3
- **UI 框架**：Element Plus
- **状态管理**：Pinia
- **路由管理**：Vue Router
- **国际化**：vue-i18n

## 功能特点

### 1. 用户权限管理
- 基于 Casbin 的 RBAC 权限模型
- 多维度数据权限控制
- 动态路由和菜单权限
- 按钮级权限控制

### 2. 系统功能
- 用户管理：用户信息管理、状态控制、多角色分配
- 角色管理：角色权限分配、数据权限设置
- 菜单管理：动态菜单配置，支持多级菜单
- 部门管理：部门组织架构维护
- 岗位管理：岗位信息维护

### 3. 系统监控
- 操作日志：系统操作记录
- 任务监控：定时任务执行监控
- 服务监控：服务器性能监控

### 4. 系统工具
- 数据字典：系统中各种枚举数据维护
- 消息管理：系统消息推送和管理

## 部署说明

### 环境要求
- Python 3.9+
- Node.js 16+
- MySQL 8.0+
- Redis
- Docker（可选）

### 部署步骤

#### 1. Docker 部署（推荐）

```bash
# 启动所有服务
docker-compose up -d

# 仅启动后端服务
docker-compose -f django-admin.yml up -d

# 仅启动前端服务
docker-compose -f django-web.yml up -d
```

#### 2. 常规部署

##### 后端部署
```bash
# 安装依赖
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 初始化数据
python manage.py init

# 启动服务
python manage.py runserver 127.0.0.1:8000
```

##### 前端部署
```bash
# 安装依赖
pnpm install

# 开发环境
pnpm dev

# 生产环境
pnpm build
```

### 初始账号
- 用户名：paopao
- 密码：123456

## 开发指南

### 后端开发
- 遵循 Django 开发规范
- 使用 Django REST framework 开发 API
- 使用 Casbin 进行权限控制
- 使用 Celery 处理异步任务

### 前端开发
- 组件命名采用 PascalCase
- TypeScript 类型定义放在 types 目录
- API 接口按模块组织在 api 目录
- 使用 ESLint + Prettier 进行代码规范

## 贡献指南

欢迎提交 Issue 或 Pull Request 来帮助改进项目。在提交之前，请确保：

1. Issue 没有被重复提交
2. Pull Request 遵循项目代码规范
3. 更新相关文档
4. 编写必要的测试用例

## 许可证

[MIT License](LICENSE)
