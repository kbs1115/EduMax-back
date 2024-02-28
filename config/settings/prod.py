from .base import *
from dotenv import load_dotenv

load_dotenv(verbose=True)

ALLOWED_HOSTS = ["13.124.25.141"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("DB_NAME"),
        "USER": "admin",
        "PASSWORD": os.getenv("RDS_DB_PASSWORD"),
        "HOST": "database-edumax.cdommqogw444.ap-northeast-2.rds.amazonaws.com",
        "PORT": "3306",
    }
}

DEBUG = False
