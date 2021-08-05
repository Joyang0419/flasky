from flask import render_template, request, redirect, url_for, make_response
from flask_login import login_required
from . import main
from app import cache
# models
from app.models.roles import Roles, Permission
from app.models.posts import Posts
# 權限
from app.decorators.permission import admin_required, permission_required
from flask_login import current_user


@main.route('/', methods=['GET', 'POST'])
# @login_required
def index():
    """首頁"""
    # Roles.insert_role()
    # show_followed預設followed
    show_followed = False
    if current_user.is_authenticated:
        # 使用者登入狀況下，預設: False
        show_followed = bool(request.cookies.get('show_followed', ''))
    if show_followed:
        posts = current_user.followed_posts
    else:
        posts = Posts.query
    # 取得分頁文章
    current_page = request.args.get('page', 1, type=int)
    pagination = posts.order_by(Posts.timestamp.desc()).paginate(
        page=current_page,
        per_page=1,
        error_out=False
    )
    # 使用form表單，新增post
    if request.method == "POST" \
            and current_user.can(Permission.WRITE):
        form_data = request.form.to_dict()
        # 新增文章
        Posts.create(
            user_id=current_user.id,
            body=form_data['body']
        )
        return redirect(url_for('main.index'))
    return render_template('index.html', pagination=pagination)


@main.route('/admin')
@login_required
@admin_required
def for_admin():
    return "for admin"


@main.route('/moderate')
@login_required
@permission_required(permission=Permission.MODERATE)
def for_moderators():
    return "for moderators"


@main.route('/test/redis/<value>')
@cache.memoize(timeout=300)
def test_redis(value):
    return value


@main.route('/show_all')
@login_required
def show_all():
    """cookie"""
    response = make_response(redirect(url_for('main.index')))
    response.set_cookie('show_followed', value='', max_age=60*60*24*30)  # 30 days
    return response


@main.route('/show_followed')
@login_required
def show_followed():
    """cookie"""
    response = make_response(redirect(url_for('main.index')))
    response.set_cookie('show_followed', value='1', max_age=60)  # 30 days
    return response


