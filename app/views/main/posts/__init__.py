from flask import Blueprint, render_template, request, url_for, redirect,abort
from flask_login import login_required, current_user
from datetime import datetime
# models
from app.models.posts import Posts
from app.models.users import Users
from app.models.roles import Roles, Permission
from app.models.comments import Comments, db
# service
from app.services.sqlalchemy_service import object_as_dict
from app.decorators.permission import permission_required_myself
# 權限
from app.decorators.permission import admin_required, permission_required

posts = Blueprint('posts', __name__)


@posts.route('/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def search_post(post_id: int):
    post = Posts.query.get_or_404(post_id)
    # endpoint
    endpoint = request.endpoint
    # 取得分頁文章
    current_page = request.args.get('page', 1, type=int)
    if current_page == -1:
        # 最新的一頁計算方式: (總評論數量 - 1) // 每頁數量得到商，在 + 1
        current_page = (post.comments.count() - 1) // 1 + 1
    pagination = post.comments.filter_by(disabled=False).order_by(Comments.timestamp.asc()).paginate(
        page=current_page,
        per_page=1,
        error_out=False
    )
    # 使用form表單，新增comment
    if request.method == "POST" \
            and current_user.can(Permission.WRITE):
        form_data = request.form.to_dict()
        # 新增文章
        Comments.create(
            post_id=post.id,
            user_id=current_user.id,
            body=form_data['body']
        )
        # page = -1的原因是為了永遠看到最新的評論。
        return redirect(url_for('posts.search_post', post_id=post_id, page=-1))
    # output_value: 前端要用到的資料
    output_value = {
        'post': post,
        'pagination': pagination,
        'endpoint': endpoint
    }
    return render_template('posts/post.html', **output_value)


@posts.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id: int):
    post = Posts.query.get_or_404(post_id)
    if request.method == 'POST':
        form_data = request.form.to_dict()
        # 修改文章
        post.update_attr(
            body=form_data['body'],
            timestamp=datetime.now()
        )
        return redirect(url_for('posts.edit_post', post_id=post_id))
    # 確認權限為最大管理者，或作者才能修改。
    if current_user != post.users and \
            not current_user.can(Permission.ADMIN):
        abort(404)
    output_value = {
        'post': post,
    }
    return render_template('posts/edit.html', **output_value)


@posts.route('/post/<int:post_id>/comments', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.MODERATE)
def post_comments(post_id: int):
    """文章全部的評論，修改disabled介面"""
    post = Posts.query.get_or_404(post_id)
    comments = post.comments
    # 取得分頁文章
    current_page = request.args.get('page', 1, type=int)
    pagination = comments.order_by(Comments.timestamp.asc()).paginate(
        page=current_page,
        per_page=1,
        error_out=False
    )
    # endpoint
    endpoint = request.endpoint
    # output_value: 前端要用到的資料
    output_value = {
        'post': post,
        'pagination': pagination,
        'endpoint': endpoint
    }
    return render_template('posts/comments.html', **output_value)


