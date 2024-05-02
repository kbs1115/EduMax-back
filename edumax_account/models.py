from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from edumax_account.model.model_manager import UserManager
from edumax_account.validators import UserValidator


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
    fcm_token = models.CharField(max_length=255, null=True, default=None)
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


class EmailTemporaryKey(models.Model):
    """
    이메일 인증을 위한 임시키저장 모델
    """
    email = models.EmailField(max_length=30, null=False, blank=False)
    key = models.CharField(max_length=6, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)


class PwChangeTemporaryQueryParam(models.Model):
    """
    패스워드 변경 페이지의 쿼리파라매터를 위한 임시 파라매터 모델
    """
    email = models.EmailField(max_length=30, null=False, blank=False)
    query_param = models.CharField(max_length=8, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
