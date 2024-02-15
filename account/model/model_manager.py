from django.contrib.auth.base_user import BaseUserManager


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
