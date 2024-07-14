from .base import *
from dotenv import load_dotenv

load_dotenv(verbose=True)

ALLOWED_HOSTS = []

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("DB_NAME"),
        "USER": "admin",
        "PASSWORD": os.getenv("LOCAL_DB_PASSWORD"),
        "HOST": "127.0.0.1",  # Use IP instead of 'localhost'
        "PORT": "3306",
    }
}

DEBUG = False

print("Using prod settings")
