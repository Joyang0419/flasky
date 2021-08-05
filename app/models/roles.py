from .db_abstract import DBAbstract
from app import db


class Roles(DBAbstract):
    """使用者角色"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64),unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    # relationship
    users = db.relationship('Users', backref='roles', lazy='dynamic')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_role():
        """資料庫內建立角色"""
        roles = {
            'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            'Moderator': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE],
            'Admin': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE, Permission.ADMIN]
        }
        default_role = 'User'
        print(default_role)
        for each_role in roles:
            role = Roles.query.filter_by(name=each_role).first()
            if role is None:
                role = Roles(name=each_role)
                role.reset_permission()
                for each_permission in roles[each_role]:
                    role.add_permission(permission=each_permission)
                role.default = (role.name == default_role)
                db.session.add(role)
        db.session.commit()

    def add_permission(self, permission: int) -> None:
        """加入權限

        :param permission: 權限
        :return: None
        """
        if not self.has_permission(permission):
            self.permissions += permission

    def remove_permission(self, permission: int) -> None:
        """刪除權限

        :param permission: 權限
        :return: None
        """
        if self.has_permission(permission):
            self.permissions -= permission

    def reset_permission(self) -> None:
        """重製權限

        :return: None
        """
        self.permissions = 0

    def has_permission(self, permission) -> bool:
        """確認使用者權限

        :param permission: 權限
        :return: bool
        """
        return self.permissions & permission == permission


class Permission:
    # 使用者權限
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16
