from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_caching import Cache
from flask_migrate import Migrate
from config import config
from flask_moment import Moment
from flaskext.markdown import Markdown

# 工具
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
# 設定Cache
cache = Cache()
mail = Mail()
migrate = Migrate()


def create_app(config_name, celery=None):
    app = Flask(__name__)
    app.config.from_object(config[config_name])  # 取得組態物件
    app.debug = config[config_name].DEBUG  # debug mode
    # 工具實例化
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    Markdown(app)
    # models
    from app.models import (
        roles,
        users,
        posts,
        follow,
        comments
    )
    migrate.init_app(app, db)
    # 啟用Cache
    cache.init_app(app)
    if celery is None:
        # routes
        from app.views.main import main as main_blueprint
        app.register_blueprint(main_blueprint)
        from app.views.auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint, url_prefix='/auth')
        from app.views.main.users import users as users_blueprint
        app.register_blueprint(users_blueprint, url_prefix='/users')
        from app.views.main.posts import posts as posts_blueprint
        app.register_blueprint(posts_blueprint, url_prefix='/posts')
    return app
