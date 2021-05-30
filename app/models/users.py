from app import db
from flask_login import UserMixin


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # 密碼雜湊化
    password_hash = db.Column(db.String(100), nullable=False)
    # confirmed
    confirmed = db.Column(db.Boolean, default=False)