from django.core.validators import RegexValidator
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

from rest_framework import exceptions


class UserValidator:
    idValidator = RegexValidator(
        regex=r"^[a-zA-Z0-9]{4,16}$",
        message="ID는 알파벳 대소문자나 숫자만을 포함하는 4~16자의 문자열이어야 합니다.",
    )
    nicknameValidator = RegexValidator(
        regex=r"^[a-zA-Z0-9가-힣]{2,10}$",
        message="닉네임은 영문, 숫자, 한글로 이루어진 2~10자의 문자열이어야 합니다.",
    )


#  중복체크를 위한 validate model
class UserUniqueFieldModel(BaseModel):
    nickname: str = Field(default=None)
    login_id: str = Field(default=None)
    email: str = Field(default=None)


#  email sending 을 위한 validate model
class EmailFieldModel(BaseModel):
    email: EmailStr = Field(max_length=30)


class EmailCheckFieldModel(BaseModel):
    email: EmailStr = Field(max_length=30)
    auth_key: str = Field(max_length=6)


class SignupParamModel(BaseModel):
    login_id: str
    email: str
    nickname: str
    password: str


class LoginParamModel(BaseModel):
    login_id: str
    password: str


class PatchUserModel(BaseModel):
    email: Optional[str] = None
    nickname: Optional[str] = None


class PasswordPageQueryParamModel(BaseModel):
    """
    패스워드 변경 페이지의 쿼리 파라매터와
    db의 쿼리 파라매터를 비교한다.
    """

    verify: str

    def __init__(self, **data):
        super().__init__(**data)
        from edumax_account.model.user_access import check_pw_change_page_query_param

        check_pw_change_page_query_param(self.verify)


class PasswordModel(BaseModel):
    """
    패스워드 변경을 위한 validator model
    """

    new_pw: str
    email: EmailStr = Field(max_length=30)
