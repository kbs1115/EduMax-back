from .base import *
from dotenv import load_dotenv

load_dotenv(verbose=True)

ALLOWED_HOSTS = []

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
print("Using local settings")