from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app import db
from app.models import User
from werkzeug.security import check_password_hash

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

# 这个函数是给 Flask-Login 用的，根据用户 ID 获取用户对象
from app import login_manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))