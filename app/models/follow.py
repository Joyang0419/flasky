from .db_abstract import DBAbstract
from app import db
from datetime import datetime
# html清洗驗證
from markdown import markdown
import bleach


class Follow(DBAbstract):
    """追隨者"""
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)

