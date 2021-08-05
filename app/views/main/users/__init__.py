from flask import Blueprint, render_template, request, url_for, redirect, abort, session
from flask_login import login_required, current_user
# models
from app.models.posts import Posts
from app.models.users import Users
from app.models.roles import Roles, Permission
# service
from app.services.sqlalchemy_service import object_as_dict
from app.decorators.permission import permission_required_myself
# 權限
from app.decorators.permission import admin_required, permission_required
# service
from app.services.sqlalchemy_service import object_as_dict

users = Blueprint('users', __name__)


@users.route('/profile/<user_uuid>', methods=['GET', 'POST'])
@login_required
def profile(user_uuid: str):
    # permission_required_myself(user_uuid=user_uuid)
    user = Users.query.filter_by(uuid=user_uuid).first()
    # 設置session
    session['user'] = object_as_dict(user)
    posts = user.posts.order_by(Posts.timestamp.desc()).all()
    if request.method == 'POST':
        data = request.form.to_dict()
        user.update_attr(**data)
        return redirect(url_for('users.profile', user_uuid=user_uuid))

    output_value = {
        'user': user,
        'posts': posts
    }
    return render_template('profile.html', **output_value)


@users.route('/admin/<string:user_uuid>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_profile(user_uuid):
    user = Users.query.filter_by(uuid=user_uuid).first()
    return object_as_dict(user)


@users.route('/follow/<string:user_uuid>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.FOLLOW)
def follow(user_uuid):
    """使用者已追蹤的話 => 取消，
    使用者未追蹤 => 追蹤
    """
    user = Users.query.filter_by(uuid=user_uuid).first()
    if current_user.is_following(user):
        current_user.unfollow(user)
    else:
        current_user.follow(user)
    return redirect(url_for('users.profile', user_uuid=user_uuid))


@users.route('/followers', methods=['GET', 'POST'])
@login_required
def followers():
    """檢視所有追隨者"""
    # 讀取session
    session_data = session.get('user')
    user = Users.query.filter_by(uuid=session_data['uuid']).first()
    # endpoint
    endpoint = request.endpoint
    # 取得分頁文章
    current_page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page=current_page,
        per_page=1,
        error_out=False
    )
    return render_template('users/follow.html', endpoint=endpoint, pagination=pagination)


@users.route('/followed', methods=['GET', 'POST'])
@login_required
def followed():
    """檢視所有跟蹤的對象"""
    # 讀取session
    session_data = session.get('user')
    user = Users.query.filter_by(uuid=session_data['uuid']).first()
    # endpoint
    endpoint = request.endpoint
    # 取得分頁文章
    current_page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page=current_page,
        per_page=1,
        error_out=False
    )
    return render_template('users/follow.html', endpoint=endpoint, pagination=pagination)
