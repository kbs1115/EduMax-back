import random
import string
from datetime import timedelta, datetime, timezone

from django.db import transaction
from rest_framework import exceptions
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from account.model.temp_access import create_password_change_param_model_inst
from account.model.user_access import get_user_with_email, check_user_exists_with_field, delete_user_db, \
    set_password
from account.service.email_service import EmailService
from account.tasks import delete_query_param_instance
from account.serializers import *


# 회원가입
class SignUpService:
    @classmethod
    def check_duplicate_field_value(
            cls,
            login_id=None,
            email=None,
            nickname=None
    ):
        """
        회원가입시 필수필드 중복체크를 위한 메소드
        한번에 여러개도 가능하고, 하나씩도 가능하다
        """
        if login_id is not None:
            return check_user_exists_with_field(User.USERNAME_FIELD, login_id)
        elif email is not None:
            return check_user_exists_with_field(User.EMAIL_FIELD, email)
        elif nickname is not None:
            return check_user_exists_with_field(User.NICKNAME_FIELD, nickname)
        else:
            raise exceptions.APIException("there is no field")

    def create_user(self, data):
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return serializer.validated_data
        else:
            raise exceptions.ValidationError(serializer.errors)


class UserService:

    @classmethod
    def get_me(cls, request):
        """
        로그인 상태의 user가 본인의 user instance를 가져올때 쓰인다.
        """
        user = request.user
        if user is None:
            raise exceptions.NotFound("user not found")

        return user

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
        delete_user_db(user)

    @staticmethod
    def generate_random_string(length=8):
        """
        user/pw-change/?verify= 의 쿼리 파라매터 만드는대 쓰인다
        """
        characters = string.ascii_letters + string.digits

        random_string = ''.join(random.choice(characters) for _ in range(length))
        return random_string

    @classmethod
    def get_user_with_email_auth(cls, email, auth_key):
        """
        비로그인 유저가 user instance를 요청할때
        이메일 인증을 통해서 본인의 user instance를 받을수있다.
        """
        if EmailService().check_authentication(email=email, auth_key=auth_key):
            return get_user_with_email(email=email)

    def make_random_query_param_with_email_auth(self, email, auth_key):
        """
        이메일 인증이 성공할시 임의의 8자리 string을 db에 1분동안 임시저장후
        string 을 return 한다.
        string은 user/pw-change/?vertify 의 query param을 만드는대 쓰인다.
        """
        if EmailService().check_authentication(email=email, auth_key=auth_key):
            random_query_params = self.generate_random_string()

            with transaction.atomic():
                inst = create_password_change_param_model_inst(email, random_query_params)

                eta = datetime.now(timezone.utc) + timedelta(minutes=1)
                delete_query_param_instance.apply_async((inst.id,), eta=eta)  # 1분후에 worker에게 삭제 명령
            return random_query_params

    def change_password(self, pw, email):
        """
        pw 를 수정한다.
        """
        user = get_user_with_email(email=email)
        set_password(user=user, pw=pw)


class AuthService:
    def loginService(self, data):

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
