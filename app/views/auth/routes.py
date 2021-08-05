from flask import render_template, request, url_for, redirect, current_app
from flask_login import current_user, login_required, logout_user, login_user
from . import auth
from app.models.users import Users
from app.models.roles import Roles
# 編譯密碼工具
from app import bcrypt
# 寄信工具
# from app.utils import send_email
from app import db
# celery send email
from app.tasks.send_email import send_email


@auth.route('/unconfirmed')
def unconfirmed():
    """使用者尚未前往email點選確認"""
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return "unconfirmed"


@auth.route('/email_confirm/<token>')
@login_required
def email_confirm(token):
    """信件驗證token

    :param token: token
    """
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.check_token(token):
        pass
        db.session.commit()
    else:
        return 'Invalid token'
    return redirect(url_for('main.index'))


@auth.route('/resend_confirmation')
@login_required
def resend_confirmation():
    """重新發送驗證信"""
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, url_for('auth.email_confirm', token=token, _external=True))
    return redirect(url_for('main.index'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """登入頁面"""
    if request.method == 'POST':
        # 拿取前端Form data
        data = request.form.to_dict()
        # 使用者驗證
        user = Users.query.filter_by(email=data['user_email']).first()
        if user is not None and user.check_password_hash(password=data['password']):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            if next_page is None or not next_page.startswith('/'):
                next_page = url_for('main.index')
            return redirect(next_page)
        return 'wrong password or e-mail'
    return render_template('auth/login.html')


@auth.route('/logout')
@login_required
def logout():
    """登出"""
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """註冊"""
    if request.method == 'POST':
        # 拿取前端Form data
        data = request.form.to_dict()
        # 驗證使用者是否存在
        user = Users.query.filter_by(email=data['user_email']).first()
        if user is not None:
            return 'Existed user e-mail'
        # create user
        user = Users.create(
            username=data['username'],
            email=data['user_email'],
            password_hash=bcrypt.generate_password_hash(data['password']).decode('utf8'),
        )
        user.generate_uuid()
        token = user.generate_confirmation_token()
        # celery send_email
        send_email.delay(user.email, url_for('auth.email_confirm', token=token, _external=True))
        return user.email
    return render_template('auth/register.html')
