# python套件庫
import os
# 引入app, db
from app import create_app, db

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
