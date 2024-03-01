from .base import *
from dotenv import load_dotenv

load_dotenv(verbose=True)

ALLOWED_HOSTS = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "edumax",
        "USER": "root",
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": "127.0.0.1",
        "PORT": "3306",
    }
}
