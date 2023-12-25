from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    id = models.AutoField(primary_key=True, db_column="id")
    username = models.CharField(max_length=20, unique=True)  # login ID 역할을 한다.
    email = models.EmailField(max_length=255, unique=True)
    nickname = models.CharField(max_length=10, unique=True)
