from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app import db
from app.models import Message
from datetime import datetime

message_bp = Blueprint('message', __name__)

# 首页：分页显示留言
@message_bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)   # 获取页码，默认第1页
    per_page = 5   # 每页显示5条
    pagination = Message.query.order_by(Message.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    messages = pagination.items
    return render_template('index.html', messages=messages, pagination=pagination)

# 新增留言
@message_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_msg = Message(title=title, content=content, author_id=current_user.id)
        db.session.add(new_msg)
        db.session.commit()
        flash('留言添加成功')
        return redirect(url_for('message.index'))
    return render_template('add.html')

# 修改留言
@message_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    msg = Message.query.get_or_404(id)
    # 检查是否是当前用户自己的留言
    if msg.author_id != current_user.id:
        abort(403)   # 无权限
    if request.method == 'POST':
        msg.title = request.form['title']
        msg.content = request.form['content']
        msg.updated_at = datetime.now()
        db.session.commit()
        flash('留言修改成功')
        return redirect(url_for('message.index'))
    return render_template('edit.html', message=msg)

# 删除留言
@message_bp.route('/delete/<int:id>')
@login_required
def delete(id):
    msg = Message.query.get_or_404(id)
    if msg.author_id != current_user.id:
        abort(403)
    db.session.delete(msg)
    db.session.commit()
    flash('留言已删除')
    return redirect(url_for('message.index'))

# 查看详情
@message_bp.route('/detail/<int:id>')
@login_required
def detail(id):
    msg = Message.query.get_or_404(id)
    return render_template('detail.html', message=msg)