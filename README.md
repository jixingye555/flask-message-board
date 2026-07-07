# Flask 留言板系统（message-board）

基于 Flask 的轻量级留言板 Web 应用，支持用户注册/登录、留言的增删改查与分页展示，使用 MySQL 持久化存储。

## 技术栈

- **Web 框架**：Flask 2.3.3
- **认证**：Flask-Login 0.6.2（会话登录、登录保护、用户加载器）
- **ORM**：Flask-SQLAlchemy 3.1.1 + SQLAlchemy 2.0.50
- **数据库**：MySQL（通过 PyMySQL 1.1.0 驱动）
- **密码安全**：Werkzeug 密码哈希（非明文存储）
- **架构模式**：工厂模式（`create_app`）+ Blueprint 模块化 + MVT

## 功能特性

- 用户登录 / 登出（Flask-Login 管理会话）
- 留言首页分页展示（每页 5 条，按时间倒序）
- 留言新增 / 修改 / 删除 / 查看详情
- **权限校验**：用户只能修改、删除自己的留言（否则返回 403）
- 用户表与留言表一对多关联

## 项目结构

```
message_board/
├── app/
│   ├── __init__.py            # 应用工厂 create_app()，注册蓝图
│   ├── models.py              # User / Message 模型（一对多）
│   ├── blueprints/
│   │   ├── auth.py            # 登录 / 登出
│   │   └── message.py         # 留言 增删改查 / 分页 / 详情
│   ├── static/
│   │   └── style.css
│   └── templates/             # HTML 模板
├── config.py                  # 配置（敏感信息从环境变量读取）
├── run.py                     # 入口：建表 + 初始化 admin + 启动服务
├── requirements.txt
└── .env.example               # 环境变量样例（复制为 .env 使用）
```

## 快速开始

```bash
# 1. 创建并激活虚拟环境
python -m venv .venv
source .venv/Scripts/activate        # Windows: .venv\Scripts\activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量
cp .env.example .env                 # 然后填入你的 MySQL 密码等

# 4. 准备数据库
# 在本机 MySQL 中创建数据库 flask_data

# 5. 启动
python run.py
# 访问 http://127.0.0.1:5000
# 默认管理员：admin / 123456（首次启动自动创建）
```

## 待办 / 规划

- [ ] 留言搜索功能
- [ ] 引入 Redis 缓存热门留言列表
- [ ] Docker 容器化 + 云服务器部署，提供在线 Demo

> Demo 链接：待部署后更新
