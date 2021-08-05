from app import db
from flask_login import UserMixin, AnonymousUserMixin
from flask import current_app
from datetime import datetime
# 編譯密碼工具
from werkzeug.security import generate_password_hash, check_password_hash
from app import bcrypt
from app import login_manager
from .db_abstract import DBAbstract
# token序列化工具
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# permission
from app.models.roles import Permission
# models: roles
from app.models.roles import Roles
from app.models.follow import Follow
from app.models.posts import Posts
# uuid
import uuid


class Users(DBAbstract, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    uuid = db.Column(db.String(64), unique=True, nullable=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # 密碼雜湊化
    password_hash = db.Column(db.String(100), nullable=False)
    # confirmed
    confirmed = db.Column(db.Boolean, default=False)
    # 個人資料
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.now)
    last_seen = db.Column(db.DateTime(), default=datetime.now)
    # relationship
    # users:posts = one to many
    posts = db.relationship('Posts', backref='users', lazy='dynamic')
    # followed:follow = one to many
    followed = db.relationship(
        'Follow',
        foreign_keys=[Follow.follower_id],
        backref=db.backref('follower', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    # followers:follow = one to many
    followers = db.relationship(
        'Follow',
        foreign_keys=[Follow.followed_id],
        backref=db.backref('followed', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    # users:comments = one to many
    comments = db.relationship('Comments', backref='users', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        # 更改密碼
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf8')

    @property
    def followed_posts(self):
        """返回用戶的追蹤者文章"""
        return Posts.query.join(Follow, Follow.followed_id == Posts.user_id).\
            filter(Follow.follower_id == self.id)

    @classmethod
    def create(cls, **kwargs):
        """新增"""
        obj = cls(**kwargs)
        # role
        admin_role = Roles.query.filter_by(name='Admin').first()
        default_role = Roles.query.filter_by(default=True).first()
        role = default_role
        if obj.email == current_app.config['MAIL_USERNAME']:
            role = admin_role
        obj.role_id = role.id
        db.session.add(obj)
        db.session.commit()
        obj.generate_uuid()
        return obj

    def generate_uuid(self):
        """產生uuid"""
        uuid_key = str(self.id)
        uuid_output = uuid.uuid5(uuid.NAMESPACE_DNS, uuid_key)
        self.uuid = uuid_output
        db.session.add(self)
        db.session.commit()

    def ping(self):
        """紀錄每次使用者登入時間"""
        self.last_seen = datetime.now()
        db.session.add(self)
        db.session.commit()

    def check_password_hash(self, password):
        """密碼驗證，驗證使用者輸入的密碼跟資料庫內的加密密碼是否相符

        :param password: 使用者輸入的密碼
        :return: True/False
        """
        return bcrypt.check_password_hash(self.password_hash, password)

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    def generate_confirmation_token(self, expiration=3600):
        """產生認證token"""
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def check_token(self, token):
        """驗證token"""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def can(self, permission) -> bool:
        """使用者是否有該權限

        :param permission: 權限
        :return: bool
        """
        return self.roles is not None and self.roles.has_permission(permission)

    def is_admin(self):
        return self.can(Permission.ADMIN)

    def is_following(self, user: object) -> bool:
        """確認追蹤狀態，使用者是否已追隨過user。

        :param user: 使用者物件
        :return bool
        """
        if user.id is None:
            return False
        return self.followed.filter_by(
            followed_id=user.id
        ).first() is not None

    def is_followed_by(self, user: object) -> bool:
        """確認是否被該用戶追蹤。

        :param user: 使用者物件
        :return bool
        """
        if user.id is None:
            return False
        return self.followers.filter_by(
            follower_id=user.id
        ).first() is not None

    def follow(self, user: object):
        """追蹤

        :param user: 使用者物件
        :return
        """
        if not self.is_following(user=user):
            follow = Follow(follower=self, followed=user)
            db.session.add(follow)
            db.session.commit()

    def unfollow(self, user: object):
        """退追蹤

        :param user: 使用者物件
        :return
        """
        followed = self.followed.filter_by(
            followed_id=user.id
        ).first()
        if followed:
            db.session.delete(followed)
            db.session.commit()

    class AnonymousUser(AnonymousUserMixin):
        def can(self, permission):
            return False

        def is_admin(self):
            return False

    login_manager.anonymous_user = AnonymousUser
