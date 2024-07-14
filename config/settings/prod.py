from .base import *
from dotenv import load_dotenv

load_dotenv(verbose=True)

ALLOWED_HOSTS = ["3.38.151.192"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("RDS_DB_NAME"),
        "USER": os.getenv("RDS_DB_USER"),
        "PASSWORD": os.getenv("RDS_DB_PASSWORD"),
        "HOST": os.getenv("RDS_DB_HOST"),
        "PORT": "3306",
    }
}

DEBUG = False

print("Using prod settings")