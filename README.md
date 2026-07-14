# Flask 留言板系统（Flask Message Board）

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-black)](https://flask.palletsprojects.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

一个基于 **Flask** 的轻量级留言板 Web 应用，支持用户注册 / 登录、留言的增删改查与搜索、分页展示，使用 **MySQL** 做持久化存储。项目采用工厂模式 + Blueprint 模块化架构，适合作为 Python 后端入门学习示例，也可作为简历中的全栈小项目。

## ✨ 功能特性

- **用户系统**
  - 注册 / 登录 / 登出（Flask-Login 管理会话）
  - 注册后端校验：用户名非空、密码至少 6 位、两次输入一致、用户名唯一
  - 密码使用 **Werkzeug 哈希**存储，数据库中绝不保存明文
- **留言管理**
  - 首页分页展示（每页 5 条，按发布时间倒序）
  - 新增 / 修改 / 查看详情 / 删除
  - **搜索**：支持按「标题 / 内容 / 作者名」模糊搜索（`GET /?q=关键词`，先过滤再分页）
  - **权限校验**：用户只能修改、删除自己的留言，否则返回 `403`
- **数据模型**：用户表与留言表一对多关联（`author_id` 外键）

## 🛠 技术栈

| 分类 | 技术 |
| --- | --- |
| Web 框架 | Flask 2.3.3 |
| 用户认证 | Flask-Login 0.6.2 |
| ORM | Flask-SQLAlchemy 3.1.1（底层 SQLAlchemy 2.0.50） |
| 数据库驱动 | PyMySQL 1.1.0 |
| 数据库 | MySQL 8.0 |
| 密码安全 | Werkzeug 密码哈希 |
| 配置管理 | python-dotenv（敏感信息从环境变量读取） |
| 架构模式 | 工厂模式 `create_app()` + Blueprint 模块化 + MVT |

## 📁 项目结构

```
flask-message-board/
├── app/
│   ├── __init__.py            # 应用工厂 create_app()，注册蓝图与 Flask-Login
│   ├── models.py              # User / Message 模型（一对多）
│   ├── blueprints/
│   │   ├── auth.py            # 登录 / 登出 / 注册
│   │   └── message.py         # 留言 增删改查 / 分页 / 搜索 / 详情
│   ├── static/
│   │   └── style.css
│   └── templates/             # HTML 模板（login/register/index/add/edit/detail...）
├── config.py                  # 配置（敏感信息从环境变量读取）
├── run.py                     # 入口：建表 + 初始化 admin + 启动服务
├── requirements.txt           # 依赖清单（UTF-8）
├── .env.example               # 环境变量样例（复制为 .env 使用）
├── .gitignore                 # 忽略 .env / .venv / __pycache__ 等
└── LICENSE                    # MIT License
```

## 🔗 路由一览

| 路由 | 方法 | 说明 | 访问权限 |
| --- | --- | --- | --- |
| `/` | GET | 首页：留言分页 + 搜索 | 需登录 |
| `/login` | GET / POST | 登录 | 公开 |
| `/register` | GET / POST | 注册新账号 | 公开 |
| `/logout` | GET | 登出 | 需登录 |
| `/add` | GET / POST | 发布新留言 | 需登录 |
| `/detail/<int:id>` | GET | 查看留言详情 | 需登录 |
| `/edit/<int:id>` | GET / POST | 修改留言 | 需登录 + 作者本人 |
| `/delete/<int:id>` | GET | 删除留言 | 需登录 + 作者本人 |

## 🚀 快速开始

### 1. 克隆仓库
```bash
git clone https://github.com/jixingye555/flask-message-board.git
cd flask-message-board
```

### 2. 创建并激活虚拟环境
```bash
python -m venv .venv
source .venv/Scripts/activate        # Windows（Git Bash）
# 或 .venv\Scripts\activate           # Windows（CMD / PowerShell）
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 配置环境变量
```bash
cp .env.example .env
```
然后编辑 `.env`，填入你的 MySQL 信息：
- `MYSQL_HOST` / `MYSQL_PORT`：数据库地址与端口（默认 `localhost:3307`，按你本地实际修改）
- `MYSQL_USER` / `MYSQL_PASSWORD`：数据库账号密码
- `MYSQL_DB`：数据库名（默认 `flask_data`）
- `SECRET_KEY`：Flask 会话签名密钥（随便填一段随机字符串）
- `ADMIN_PASSWORD`：默认管理员 admin 的密码（默认 `123456`，生产请修改）
- `FLASK_DEBUG`：调试模式，`1` 开 / `0` 关（部署务必 `0`）

> ⚠️ `.env` 已被 `.gitignore` 忽略，**不会**被提交到 GitHub，密码安全。

### 5. 准备数据库
在本机 MySQL 中创建数据库（名称与 `.env` 中 `MYSQL_DB` 一致）：
```sql
CREATE DATABASE flask_data CHARACTER SET utf8mb4;
```

### 6. 启动
```bash
python run.py
```
访问 http://127.0.0.1:5000 即可。
- 首次启动会自动建表，并创建默认管理员账号 `admin` / `ADMIN_PASSWORD`（默认 `123456`）。
- 普通用户可在 `/register` 页面自行注册。

## 🗺 待办 / 规划

- [x] 用户注册功能
- [x] 留言搜索功能（标题 / 内容 / 作者名模糊搜）
- [ ] 引入 Redis 缓存热门留言列表
- [ ] Docker 容器化 + 云服务器部署，提供在线 Demo
- [ ] 留言点赞 / 评论互动
- [ ] 开放 REST API

> 🔗 Demo 链接：待部署后更新

## 📄 许可证

[MIT License](LICENSE)
