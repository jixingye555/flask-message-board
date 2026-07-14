from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from sqlalchemy import or_   # 用来实现“标题 或 内容 或 作者”多条件匹配
from app import db
from app.models import Message, User   # 同时导入 User，搜索作者用户名要用
from datetime import datetime

message_bp = Blueprint('message', __name__)

# 首页：分页显示留言（支持按关键词搜索）
@message_bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)   # 获取页码，默认第1页
    per_page = 5   # 每页显示5条
    keyword = request.args.get('q', '').strip()   # 获取搜索词，strip() 去掉首尾空格

    # 1) 先拿到一个“查询对象”（此时还没真正查数据库，只是拼条件）
    query = Message.query

    # 2) 如果用户搜了东西，就加过滤条件
    if keyword:
        # join(User)：留言表通过 author_id 关联到用户表，才能按用户名搜
        # or_(...) ：满足“标题含关键词” 或 “内容含关键词” 或 “作者名含关键词” 任一即可
        # like('%xx%') ：模糊匹配，% 是通配符，表示“前后可以有任意字符”
        query = query.join(User).filter(
            or_(
                Message.title.like(f'%{keyword}%'),
                Message.content.like(f'%{keyword}%'),
                User.username.like(f'%{keyword}%')
            )
        )

    # 3) 按时间倒序分页（这一步才真正查数据库）
    pagination = query.order_by(Message.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    messages = pagination.items

    # 4) 把 keyword 也传给模板：让搜索框回显刚才输入的内容，分页链接也能带上关键词
    return render_template('index.html', messages=messages, pagination=pagination, keyword=keyword)

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