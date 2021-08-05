from functools import wraps
from flask import abort
from flask_login import current_user
from app.models.roles import Permission
from app.models.users import Users


def permission_required(permission):
    """權限判斷，若使用者無該權限，給予403頁面。"""
    def decorator(function):
        @wraps(function)
        def decorator_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return function(*args, **kwargs)
        return decorator_function
    return decorator


def permission_required_myself(user_uuid):
    """權限判斷，若使用者非本人，給予403頁面。"""
    user = Users.query.filter_by(uuid=user_uuid).first()
    if current_user != user:
        abort(403)


def admin_required(f):
    # 需要管理者權限
    return permission_required(Permission.ADMIN)(f)
