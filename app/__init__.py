from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

# 工具
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])  # 取得組態物件
    app.debug = config[config_name].DEBUG  # debug mode
    # 工具實例化
    db.init_app(app)
    # routes
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app
