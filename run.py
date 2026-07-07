import os

from app import create_app, db
from app.models import User, Message
from werkzeug.security import generate_password_hash

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Message': Message}


if __name__ == '__main__':
    with app.app_context():
        # 创建所有数据库表（如果不存在）
        db.create_all()
        # 检查是否已有 admin 用户，没有则创建。密码来自环境变量，默认 123456
        if not User.query.filter_by(username='admin').first():
            admin_pw = os.environ.get('ADMIN_PASSWORD', '123456')
            admin = User(
                username='admin',
                password=generate_password_hash(admin_pw),
            )
            db.session.add(admin)
            db.session.commit()
            print('创建默认用户 admin 成功')
    # debug 由环境变量 FLASK_DEBUG 控制，部署时务必设为 0
    app.run(
        debug=os.environ.get('FLASK_DEBUG') == '1',
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
    )
