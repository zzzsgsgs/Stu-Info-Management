# 学生信息管理系统 (Student Info Management)

这是一个现代化、全栈分离的学生信息管理系统，适合作为现代 Web 开发的脚手架项目。

## 🚀 技术栈

**后端 (Backend)**
- Python 3.10+
- FastAPI (高性能异步 Web 框架)
- SQLAlchemy (ORM 模型)
- Alembic (数据库迁移)
- SQLite (本地数据库，开箱即用)
- Pydantic (数据验证)
- JWT (鉴权认证)

**前端 (Frontend)**
- Vue 3 (Composition API)
- Vite (极速构建工具)
- Vue Router (前端路由)
- Pinia (状态管理)
- Element Plus (UI 组件库)
- ECharts (图表展示)
- Axios (HTTP 请求封装)
- Tailwind/CSS (样式布局)

## 📦 核心功能

- **基础认证**: 提供管理员登录机制，基于 JWT 进行接口鉴权。预设账号：`admin` / `admin`。
- **Dashboard (仪表盘)**: 实时统计总学生数、平均 GPA、通过 ECharts 展示性别比例（饼图）和各专业人数分布（柱状图）。
- **学生管理 (CRUD)**:
  - 列表支持 **服务端分页**、根据姓名/专业 **搜索**、根据学号/GPA 进行 **排序**。
  - 新增/编辑页面提供完整的表单校验（如：学号不可修改、GPA在0-4之间等）。
  - 支持删除学生操作。

## 🛠 本地快速启动指南

### 1. 启动后端

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 运行数据库迁移并自动注入 30 条模拟数据
alembic upgrade head
python seed.py

# 启动 FastAPI 服务
uvicorn main:app --reload
# 服务将运行在 http://127.0.0.1:8000
```

### 2. 启动前端

打开一个新的终端窗口：

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
# 服务将运行在 http://localhost:5173
```

启动完成后，访问 `http://localhost:5173`。
默认管理员账号：`admin`
默认管理员密码：`admin`

## 🧪 测试

**后端测试:**
```bash
cd backend
pytest
```

**前端测试:**
```bash
cd frontend
npm run test
```
