from flask import Blueprint
from flask_login import current_user
from flask import request, redirect, url_for

auth = Blueprint('auth', __name__)

from .import routes


@auth.before_app_request
def before_request():
    """處理未確認的帳號"""
    if current_user.is_authenticated:
        # 記錄使用者登入
        current_user.ping()
        if not current_user.confirmed \
                and request.blueprint != 'auth' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))