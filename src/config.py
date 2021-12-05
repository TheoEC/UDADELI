# from dotenv import load_dotenv
# import os
import redis
from datetime import timedelta

class ApplicationConfig:	
    SECRET_KEY = "mcvnlnafophaojrngqkrngophnfokjnbskdvcnoj"
	
    SESSION_TYPE = "redis"
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.from_url("redis://127.0.0.1:6379")
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)

    UPLOAD_EXTENSIONS = ".xlsx"
