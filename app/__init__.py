from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# 创建数据库对象和登录管理对象（先不绑定到 app）
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'   # 未登录时跳转到登录页面

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)   # 加载配置

    # 把 db 和 login_manager 和 app 关联起来
    db.init_app(app)
    login_manager.init_app(app)

    # 导入蓝图（后面会创建）
    from app.blueprints.auth import auth_bp
    from app.blueprints.message import message_bp

    # 注册蓝图，给每个蓝图一个 URL 前缀
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(message_bp, url_prefix='/')

    return app