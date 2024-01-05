from django.core.validators import RegexValidator
from django.contrib.auth.base_user import BaseUserManager


class UserValidator:
    idValidator = RegexValidator(
        regex=r"^[a-zA-Z0-9]{4,16}$",
        message="ID는 알파벳 대소문자나 숫자만을 포함하는 4~16자의 문자열이어야 합니다.",
    )
    nicknameValidator = RegexValidator(
        regex=r"^[a-zA-Z0-9가-힣]{2,10}$",
        message="닉네임은 영문, 숫자, 한글로 이루어진 2~10자의 문자열이어야 합니다.",
    )


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, login_id, email, nickname, password):
        if not login_id:
            raise ValueError("must have a login_id")
        if not email:
            raise ValueError("must have an email address")
        if not nickname:
            raise ValueError("must have a nickname")
        if not password:
            raise ValueError("must have a password")

        user = self.model(
            login_id=login_id,
            email=self.normalize_email(email),
            nickname=nickname,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login_id, email, nickname, password):
        superuser = self.create_user(
            login_id=login_id,
            email=email,
            nickname=nickname,
            password=password,
        )
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True
        superuser.save(using=self._db)
        return superuser
