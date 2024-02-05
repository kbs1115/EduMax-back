from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from .domain import UserManager
from .validators import UserValidator


class User(AbstractBaseUser, PermissionsMixin):
    login_id = models.CharField(
        max_length=20,
        validators=[UserValidator.idValidator],
        unique=True,
        null=False,
        blank=False,
    )
    email = models.EmailField(max_length=30, unique=True, null=False, blank=False)
    nickname = models.CharField(
        max_length=20,
        validators=[UserValidator.nicknameValidator],
        unique=True,
        null=False,
        blank=False,
    )
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    NICKNAME_FIELD = "nickname"
    USERNAME_FIELD = "login_id"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email", "nickname"]

    class Meta:
        db_table = "user"
