from .db_abstract import DBAbstract
from app import db
from datetime import datetime
# html清洗驗證
from markdown import markdown
import bleach


class Posts(DBAbstract):
    """文章"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
    # relationship
    # posts:comments = one to many
    comments = db.relationship('Comments', backref='posts', lazy='dynamic')

    @staticmethod
    def on_change_body(target, value, old_value, initiator):
        """markdown html清洗驗證"""
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote',
                        'code', 'em', 'i', 'li', 'ol',
                        'pre', 'strong', 'ul', 'h1', 'h2',
                        'h3', 'p']
        target.body_html = bleach.linkify(
            bleach.clean(
                markdown(value, output_format='html'),
                tags=allowed_tags,
                strip=True
            )
        )


# db sqlalchemy 監聽器: Posts.body改變時執行。
db.event.listen(Posts.body, 'set', Posts.on_change_body)
