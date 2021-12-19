import os
import redis
from datetime import timedelta


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    # UPLOAD_PATH = 'uploads'

    SESSION_TYPE = "redis"
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.from_url("redis://127.0.0.1:6379")
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)

    UPLOAD_EXTENSIONS = ".xlsx"

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


env_config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    # "production": ProductionConfig,
}
