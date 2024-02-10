import random
from datetime import timedelta, datetime, timezone
from smtplib import SMTPException

from django.db import transaction
from rest_framework import exceptions, permissions, status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.mail import EmailMessage
from account.tasks import delete_email_key_instance
from account.models import EmailTemporaryKey
from account.serializers import *
from config.settings import EMAIL_HOST_USER


class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return not request.user.is_authenticated
        else:
            return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user:
            if obj.id == request.user.id:
                return True
            raise exceptions.PermissionDenied()
        raise exceptions.NotAuthenticated()


class SignUpService:
    def create_user(data):
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return serializer.validated_data
        else:
            raise exceptions.ValidationError(serializer.errors)

    def check_duplicate_field_value(
            self,
            login_id=None,
            email=None,
            nickname=None
    ):
        if login_id is not None:
            return UserService.user_exists_with_field(User.USERNAME_FIELD, login_id)
        elif email is not None:
            return UserService.user_exists_with_field(User.EMAIL_FIELD, email)
        elif nickname is not None:
            return UserService.user_exists_with_field(User.NICKNAME_FIELD, nickname)
        else:
            raise exceptions.APIException("there is no field")


class UserService:
    @classmethod
    def user_exists_with_field(cls, field, value):
        if field == User.EMAIL_FIELD:
            return User.objects.filter(email=value).exists()
        elif field == User.NICKNAME_FIELD:
            return User.objects.filter(nickname=value).exists()
        elif field == User.USERNAME_FIELD:
            return User.objects.filter(login_id=value).exists()

    @classmethod
    def get_me(cls, request):
        user = request.user
        if user is None:
            raise exceptions.NotFound("user not found")

        return user

    @classmethod
    def get_user_with_pk(cls, pk):
        try:
            return User.objects.get(id=pk)
        except User.DoesNotExist:
            raise exceptions.NotFound("user not found")

    @classmethod
    def get_serializer_data(cls, user):
        serializer = UserSerializer(user)
        return serializer.data

    @classmethod
    def update_user(cls, user, data):
        serializer = UserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        else:
            raise exceptions.ValidationError(serializer.errors)

    @classmethod
    def delete_user(cls, user):
        try:
            user.delete()
        except:
            raise exceptions.APIException("deletion failed")


class AuthService:
    def loginService(data):
        user = authenticate(
            login_id=data.get("login_id"), password=data.get("password")
        )

        if user:
            serializer = UserSerializer(user)

            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)

            return {
                "userData": serializer.data,
                "refreshToken": refresh_token,
                "accessToken": access_token,
            }
        else:
            raise exceptions.ValidationError(
                "The provided information does not match any user."
            )


class EmailService:
    @classmethod
    def generate_random_number(cls):
        return ''.join(random.choice('0123456789') for _ in range(6))

    @classmethod
    def create_email_key_model_instance(cls, email, auth_key):
        return EmailTemporaryKey.objects.create(email=email, key=auth_key)

    @classmethod
    def validate_email_key(cls, email, auth_key):
        queryset = EmailTemporaryKey.objects.filter(email=email)
        if queryset.exists():
            email_key_instance = queryset.latest('created_at')
            if email_key_instance.key == auth_key:
                return True
            else:
                raise exceptions.ValidationError(
                    "인증번호가 틀렸습니다."
                )
        else:
            raise exceptions.ValidationError(  # 물론 이부분은 프론트에서 이메일 전송을 안누르면 인증하기를 불가능하게 만들어놔야함
                "이메일 시간이 만료됐거나, 이메일 전송이 필요합니다."
            )

    """
    추가로 고려해줘야할점:
    1. 이메일 전송 제한을 걸어야함.(기준은 ip, 혹은 토큰이 될거같음)->service 단 validator
    """
    def send_email(self, email):
        subject = "EduMax 이메일 인증"  # 타이틀
        to = [email]  # 수신할 이메일 주소
        from_email = EMAIL_HOST_USER  # 발신할 이메일 주소
        auth_key = self.generate_random_number()
        message = f"인증번호: \n{auth_key}"  # 본문 내용

        try:
            with transaction.atomic():
                inst = self.create_email_key_model_instance(email, auth_key)
                EmailMessage(
                    subject=subject,
                    body=message,
                    to=to,
                    from_email=from_email
                ).send()  # 만약 없는 메일이라고 하면 아무런 응답이 없음 에러도 안뜸

                eta = datetime.now(timezone.utc) + timedelta(minutes=5)
                delete_email_key_instance.apply_async((inst.id,), eta=eta)  # 5분후에 worker에게 삭제 명령
                return {"message": "email sent successfully", "status_code": status.HTTP_200_OK}
        except SMTPException as e:
            raise exceptions.APIException(str(e))

    """
        추가로 고려해줘야할점:
        1. 횟수제한 걸어야함.(3번이상 틀리면 ip차단시킨다던가) ->service 단 validator
    """
    def check_authentication(self, email, auth_key):
        if self.validate_email_key(email=email, auth_key=auth_key):
            return {"message": "email authenticated successfully", "status_code": status.HTTP_200_OK}











