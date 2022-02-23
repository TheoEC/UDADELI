import os
import redis
from datetime import timedelta


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')

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


class ProductionConfig(Config):
    SESSION_REDIS = redis.from_url("redis://127.0.0.1:6379")


env_config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
