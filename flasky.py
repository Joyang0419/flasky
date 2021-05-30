# python套件庫
import os
from flask_migrate import Migrate
# 引用models
from app.models import (
    users
)
# 引入app, db
from app import create_app, db

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)
