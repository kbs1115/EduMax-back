from django.core.validators import RegexValidator
from pydantic import BaseModel
from typing import Optional


class UserValidator:
    idValidator = RegexValidator(
        regex=r"^[a-zA-Z0-9]{4,16}$",
        message="ID는 알파벳 대소문자나 숫자만을 포함하는 4~16자의 문자열이어야 합니다.",
    )
    nicknameValidator = RegexValidator(
        regex=r"^[a-zA-Z0-9가-힣]{2,10}$",
        message="닉네임은 영문, 숫자, 한글로 이루어진 2~10자의 문자열이어야 합니다.",
    )


class SignupParamModel(BaseModel):
    login_id: str
    email: str
    nickname: str
    password: str


class LoginParamModel(BaseModel):
    login_id: str
    password: str


class PatchUserModel(BaseModel):
    email: Optional[str]
    nickname: Optional[str]
