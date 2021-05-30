import os
from dotenv import load_dotenv

# 抓取env檔案位置。
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

# 若env檔案位置存在，讀取環境變數。
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


# Config基礎類別：所有組態共同的設定
class Config:
    # 密鑰
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'  # 可以從環境變數匯入，或是使用預設值
    # e-mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googleapis.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_SUBJECT_PREFIX = os.environ.get('MAIL_SUBJECT_PREFIX')
    MAIL_DEFAULT_SENDER = (os.getenv('MAIL_USER'), os.getenv('MAIL_USERNAME'))
    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 實作空的init_app()方法
    @staticmethod
    def init_app(app):
        pass


# 子類別：分別定義特定組態專屬的設定，讓app在各個組態設置中使用不同的資料庫
class DevelopmentConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


# 將各種組態註冊到config字典
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig  # 將Development組態，註冊為預設值
}