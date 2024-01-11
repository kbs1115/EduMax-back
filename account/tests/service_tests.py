import pytest
from account.serializers import UserSerializer
from account.services import SignUpService
from unittest.mock import Mock
from rest_framework import exceptions
from rest_framework.validators import UniqueValidator


@pytest.fixture
def valid_request_data():
    # 유효한 request 데이터를 반환한다.
    return {
        "login_id": "bruce1118",
        "email": "bruce1118@naver.com",
        "nickname": "KBS3",
        "password": "Bb3848948389!!!",
    }


@pytest.fixture
def invalid_request_data_omitted():
    # 유효하지 않은 request 데이터를 반환한다.
    return {
        "login_id": None,
        "email": "bruce1118@naver.com",
        "nickname": "KBS3",
        "password": "Bb3848948389!!!",
    }


@pytest.fixture
def invalid_request_data_wrong_email():
    # 유효하지 않은 request 데이터를 반환한다.
    return {
        "login_id": "bruce1118",
        "email": "bruce1118naver.com",
        "nickname": "KBS3",
        "password": "Bb3848948389!!!",
    }


class TestSignUpService:
    def test_signup_with_valid_user_data(self, valid_request_data, mocker):
        mock_request = Mock(data=valid_request_data)
        mock_save = mocker.patch.object(UserSerializer, "save")
        mocker.patch.object(
            UniqueValidator, "__call__"
        )  # unique 조건을 test하는 Validator의 __call__ method를 mocking한다.

        serializer = UserSerializer(data=valid_request_data)
        assert serializer.is_valid() == True
        validated_data = serializer.validated_data

        result = SignUpService.get_user_data(mock_request)

        # save 호출 여부를 확인하고, validated_data를 잘 반환하는지 테스트한다.
        mock_save.assert_called_once()
        assert validated_data == result

    def test_signup_with_omitted_user_data(self, invalid_request_data_omitted, mocker):
        mock_request = Mock(data=invalid_request_data_omitted)
        mock_save = mocker.patch.object(UserSerializer, "save")
        mocker.patch.object(
            UniqueValidator, "__call__"
        )  # unique 조건을 test하는 Validator의 __call__ method를 mocking한다.

        with pytest.raises(exceptions.ParseError):
            SignUpService.get_user_data(mock_request)

    def test_signup_with_wrong_email_user_data(
        self, invalid_request_data_wrong_email, mocker
    ):
        mock_request = Mock(data=invalid_request_data_wrong_email)
        mock_save = mocker.patch.object(UserSerializer, "save")
        mocker.patch.object(
            UniqueValidator, "__call__"
        )  # unique 조건을 test하는 Validator의 __call__ method를 mocking한다.

        with pytest.raises(exceptions.ParseError):
            SignUpService.get_user_data(mock_request)
