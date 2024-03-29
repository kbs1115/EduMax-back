from .base import *
from dotenv import load_dotenv

load_dotenv(verbose=True)

ALLOWED_HOSTS = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "edumaxdb",
        "USER": "root",
        "PASSWORD": os.getenv("DB_PASSWORD", "rootpassword"),
        "HOST": "127.0.0.1",
        "PORT": "3306",
    }
}
