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
    # Mail-SMTP Server 設定
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_DEBUG = 0
    MAIL_USE_SSL = True
    MAIL_DEFAULT_SENDER = ('Joy', 'joe_1201@reddoor.com.tw'),
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Cache REDIS
    CACHE_TYPE = os.getenv('CACHE_TYPE')
    CACHE_REDIS_HOST = os.getenv('REDIS_HOST')
    CACHE_REDIS_PORT = os.getenv('REDIS_PORT')
    CACHE_REDIS_DB = os.getenv('REDIS_CHANNEL')
    CACHE_KEY_PREFIX = os.getenv('CACHE_KEY_PREFIX')
    CACHE_DEFAULT_TIMEOUT = os.getenv('CACHE_DEFAULT_TIMEOUT')

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