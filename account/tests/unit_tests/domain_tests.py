import pytest
from account.domain import UserValidator
from django.core.exceptions import ValidationError
from account.models import User


@pytest.fixture
def user_data_correct():
    user_data = {
        "login_id": "bruce1115",
        "email": "kbs1115@naver.com",
        "nickname": "KBS",
        "password": "1987e498!2124Bb",
    }
    return user_data


@pytest.fixture
def user_data_wrong():
    user_data = {
        "login_id": None,
        "email": "kbs1115@naver.com",
        "nickname": "KBS",
        "password": "1987e498!2124Bb",
    }
    return user_data


class TestValidators:
    def test_idValidator(self):
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

    def test_nicknameValidator(self):
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


class TestUserManager:
    # create_user method를 호출할 때 인자가 제대로 전달되면 save를 호출하는지 확인, 아니면 error 발생하는지 확인
    def test_create_user_method_with_correct_data(self, mocker, user_data_correct):
        mock_save = mocker.patch.object(User, "save")
        User.objects.create_user(**user_data_correct)

        mock_save.assert_called_once()

    def test_create_user_method_with_wrong_data(self, mocker, user_data_wrong):
        mock_save = mocker.patch.object(User, "save")

        # login_id가 None일 때만 테스트 진행
        with pytest.raises(ValueError):
            User.objects.create_user(**user_data_wrong)

    def test_create_superuser_method_with_correct_data(self, mocker, user_data_correct):
        mock_save = mocker.patch.object(User, "save")
        superuser = User.objects.create_superuser(**user_data_correct)

        mock_save.assert_called()
        assert superuser.is_staff is True
        assert superuser.is_superuser is True
        assert superuser.is_active is True

    def test_create_superuser_method_with_wrong_data(self, mocker, user_data_wrong):
        mock_save = mocker.patch.object(User, "save")

        # login_id가 None일 때만 테스트 진행
        with pytest.raises(ValueError):
            User.objects.create_superuser(**user_data_wrong)
