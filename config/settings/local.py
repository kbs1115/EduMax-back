from .base import *

ALLOWED_HOSTS = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "edumax",
        "USER": "root",
        "PASSWORD": os.getenv("LOCAL_DB_PASSWORD"),
        "HOST": "localhost",
        "PORT": "3306",
    }
}
