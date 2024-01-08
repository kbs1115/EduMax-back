import pytest
from account.domain import UserValidator
from django.core.exceptions import ValidationError


def test_idValidator():
    validator = UserValidator.idValidator

    assert validator("aA12345") is None
    assert validator("bb123412345BB") is None

    # 글자 수 4 미만
    with pytest.raises(ValidationError):
        validator("bb1")
    # 글자 수 16 초과
    with pytest.raises(ValidationError):
        validator("bb123456789012345")
    # 특수문자 포함
    with pytest.raises(ValidationError):
        validator("bb1#123")


def test_nicknameValidator():
    validator = UserValidator.nicknameValidator

    assert validator("aA5가") is None
    assert validator("bb해1234B") is None

    # 글자 수 2 미만
    with pytest.raises(ValidationError):
        validator("나")
    # 글자 수 10 초과
    with pytest.raises(ValidationError):
        validator("12345678901")
    # 특수문자 포함
    with pytest.raises(ValidationError):
        validator("bb1#123나B")
