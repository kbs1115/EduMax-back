from django.core.validators import RegexValidator
from pydantic import BaseModel, Field, EmailStr, field_validator, root_validator, model_validator
from typing import Optional

from rest_framework import exceptions

from community.view.validation import sanitize_html, reject_html_content


class UserValidator:
    idValidator = RegexValidator(
        regex=r"^[a-zA-Z0-9_]{4,20}$",
        message="ID는 알파벳 대소문자나 숫자, '_'만을 포함하는 4~20자의 문자열이어야 합니다.",
    )
    nicknameValidator = RegexValidator(
        regex=r"^[\u3131-\u318E\uAC00-\uD7A3a-zA-Z0-9]{2,10}$",
        message="닉네임은 영문, 숫자, 한글로 이루어진 2~10자의 문자열이어야 합니다.",
    )


#  중복체크를 위한 validate model
class UserUniqueFieldModel(BaseModel):
    nickname: str = Field(default=None)
    login_id: str = Field(default=None)
    email: str = Field(default=None)

    @model_validator(mode='before')
    @classmethod
    def sanitize_all_fields(cls, values):
        for field, value in values.items():
            if isinstance(value, str):
                values[field] = reject_html_content(value)
        return values


#  email sending 을 위한 validate model
class EmailFieldModel(BaseModel):
    email: EmailStr = Field(max_length=30)

    @model_validator(mode='before')
    @classmethod
    def sanitize_all_fields(cls, values):
        for field, value in values.items():
            if isinstance(value, str):
                values[field] = reject_html_content(value)
        return values


class EmailCheckFieldModel(BaseModel):
    email: EmailStr = Field(max_length=30)
    auth_key: str = Field(max_length=6)

    @model_validator(mode='before')
    @classmethod
    def sanitize_all_fields(cls, values):
        for field, value in values.items():
            if isinstance(value, str):
                values[field] = reject_html_content(value)
        return values


class SignupParamModel(BaseModel):
    login_id: str
    email: str
    nickname: str
    password: str
    auth_key: str

    @model_validator(mode='before')
    @classmethod
    def sanitize_all_fields(cls, values):
        for field, value in values.items():
            if isinstance(value, str):
                values[field] = reject_html_content(value)
        return values


class LoginParamModel(BaseModel):
    login_id: str
    password: str

    @model_validator(mode='before')
    @classmethod
    def sanitize_all_fields(cls, values):
        for field, value in values.items():
            if isinstance(value, str):
                values[field] = reject_html_content(value)
        return values


class CanAccessUserFieldModel(BaseModel):
    login_id: Optional[bool] = False
    nickname: Optional[bool] = False
    email: Optional[bool] = False
    is_staff: Optional[bool] = False

    @model_validator(mode='before')
    @classmethod
    def sanitize_all_fields(cls, values):
        for field, value in values.items():
            if isinstance(value, str):
                values[field] = reject_html_content(value)
        return values


class PatchUserModel(BaseModel):
    email: Optional[str] = None
    nickname: Optional[str] = None

    @model_validator(mode='before')
    @classmethod
    def sanitize_all_fields(cls, values):
        for field, value in values.items():
            if isinstance(value, str):
                values[field] = reject_html_content(value)
        return values


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

    @model_validator(mode='before')
    @classmethod
    def sanitize_all_fields(cls, values):
        for field, value in values.items():
            if isinstance(value, str):
                values[field] = reject_html_content(value)
        return values
