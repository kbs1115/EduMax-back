import random
import string
from datetime import timedelta, datetime, timezone

from django.db import transaction
from rest_framework import exceptions
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from edumax_account.model.temp_access import create_password_change_param_model_inst
from edumax_account.model.user_access import (
    get_user_with_email,
    check_user_exists_with_field,
    delete_user_db,
    set_password,
    get_number_of_social_account,
)
from edumax_account.service.email_service import EmailService
from edumax_account.tasks import delete_query_param_instance
from edumax_account.serializers import *


# 회원가입
class SignUpService:
    @classmethod
    def check_duplicate_field_value(cls, login_id=None, email=None, nickname=None):
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

    @classmethod
    def create_social_user(cls, email):
        with transaction.atomic():
            # 현재는 nickname도 랜덤 설정하고 있는데, Frontend가 완성되면 회원가입창에서 받도록 할 예정
            login_id = email.split("@")[0] + UserService.generate_random_string(4)
            password = UserService.generate_random_string(12)
            nickname = UserService.generate_random_string(6)

            data = {
                "login_id": login_id,
                "password": password,
                "nickname": nickname,
                "email": email,
            }

            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                user = serializer.save()
            else:
                raise exceptions.ValidationError(serializer.errors)

            # SocialAccount instance도 생성한다. uid는 일단 숫자로?
            google_account_number = get_number_of_social_account("google")
            uid = str(google_account_number + 1)

            data = {"provider": "google", "user": user.id, "uid": uid}
            social_account_serializer = SocialAccountCreateSerializer(data=data)
            if social_account_serializer.is_valid():
                social_account_serializer.save()
            else:
                raise exceptions.ValidationError(social_account_serializer.errors)

        return user


class UserService:
    @classmethod
    def get_my_user_fields(cls, user, login_id=None, nickname=None, email=None, is_staff=None):
        require_fields = []
        if user is None:
            raise exceptions.NotAuthenticated("user_id is essential param")
        if login_id is not None:
            require_fields.append('login_id')
        if nickname is not None:
            require_fields.append('nickname')
        if email is not None:
            require_fields.append('email')
        if is_staff is not None:
            require_fields.append('is_staff')

        serializer = UserSerializer(user, fields=require_fields)

        return serializer.data

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

    # TODO: 이런거 utils 함수로 빼버리는게나은듯?
    @staticmethod
    def generate_random_string(length=8):
        """
        user/pw-change/?verify= 의 쿼리 파라매터 만드는대 쓰인다
        """
        characters = string.ascii_letters + string.digits

        random_string = "".join(random.choice(characters) for _ in range(length))
        return random_string

    @classmethod
    def get_user_with_email_auth(cls, email, auth_key):
        """
        비로그인 유저가 user instance를 요청할때
        이메일 인증을 통해서 본인의 user instance를 받을수있다.
        """
        if EmailService().check_authentication(email=email, auth_key=auth_key):
            return get_user_with_email(email=email)

    # TODO: 이거 이메알 service로 옮기는게 맞아보임
    def make_random_query_param_with_email_auth(self, email, auth_key):
        """
        이메일 인증이 성공할시 임의의 8자리 string을 db에 1분동안 임시저장후
        string 을 return 한다.
        string은 user/pw-change/?vertify 의 query param을 만드는대 쓰인다.
        """
        if EmailService().check_authentication(email=email, auth_key=auth_key):
            random_query_params = self.generate_random_string()

            with transaction.atomic():
                inst = create_password_change_param_model_inst(
                    email, random_query_params
                )

                eta = datetime.now(timezone.utc) + timedelta(minutes=1)
                delete_query_param_instance.apply_async(
                    (inst.id,), eta=eta
                )  # 1분후에 worker에게 삭제 명령
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

    @classmethod
    def social_login_service(cls, user):
        # 이미 인증 절차를 거쳤으므로 authenticate 없이 로그인을 시켜 준다.
        serializer = UserSerializer(user)

        token = TokenObtainPairSerializer.get_token(user)
        refresh_token = str(token)
        access_token = str(token.access_token)

        return {
            "userData": serializer.data,
            "refreshToken": refresh_token,
            "accessToken": access_token,
        }
