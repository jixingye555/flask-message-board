from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app import db
from app.models import User
from werkzeug.security import check_password_hash, generate_password_hash

# 创建一个蓝图对象，名字叫 auth
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # 从数据库查询用户
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)   # 记住登录状态
            return redirect(url_for('message.index'))  # 跳转到留言板首页
        else:
            flash('用户名或密码错误')
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required   # 必须登录才能登出
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        confirm = request.form.get('confirm', '')
        # 后端校验：和前端校验双保险，防止有人绕过网页直接发请求
        if not username or not password:
            flash('用户名和密码不能为空')
        elif len(password) < 6:
            flash('密码至少 6 位')
        elif password != confirm:
            flash('两次输入的密码不一致')
        elif User.query.filter_by(username=username).first():
            flash('该用户名已被注册')
        else:
            # 密码用 Werkzeug 哈希后再存库，绝不存明文（和登录时的 check_password_hash 配套）
            hashed = generate_password_hash(password)
            user = User(username=username, password=hashed)
            db.session.add(user)
            db.session.commit()
            flash('注册成功，请登录')
            return redirect(url_for('auth.login'))
    return render_template('register.html')

# 这个函数是给 Flask-Login 用的，根据用户 ID 获取用户对象
from app import login_manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))