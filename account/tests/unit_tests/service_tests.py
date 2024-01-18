import pytest
from account.tests.conftests import *
from account.serializers import UserSerializer
from account.services import SignUpService, AuthService
from account.models import User
from unittest.mock import Mock
from rest_framework import exceptions
from rest_framework.validators import UniqueValidator


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

        with pytest.raises(exceptions.ValidationError):
            SignUpService.get_user_data(mock_request)

    def test_signup_with_wrong_email_user_data(
        self, invalid_request_data_wrong_email, mocker
    ):
        mock_request = Mock(data=invalid_request_data_wrong_email)
        mock_save = mocker.patch.object(UserSerializer, "save")
        mocker.patch.object(
            UniqueValidator, "__call__"
        )  # unique 조건을 test하는 Validator의 __call__ method를 mocking한다.

        with pytest.raises(exceptions.ValidationError):
            SignUpService.get_user_data(mock_request)


class TestAuthService:
    def test_valid_login(self, valid_login_data, mocker):
        mock_request = Mock(data=valid_login_data)
        mock_authenticate = mocker.patch("account.services.authenticate")
        mock_authenticate.return_value = User(id=1)
        serializer = UserSerializer(mock_authenticate.return_value)

        actual = AuthService.loginService(mock_request)

        assert mock_authenticate.is_called_once()

        # 각 데이터가 제대로 들어왔는지 존재 여부를 확인한다.(token은 random이므로 정확히 비교하는 것은 옳지 않다.)
        assert actual["userData"] == serializer.data
        assert "accessToken" in actual
        assert "refreshToken" in actual

    def test_invalid_login(self, invalid_login_data, mocker):
        mock_request = Mock(data=invalid_login_data)
        mock_authenticate = mocker.patch("account.services.authenticate")
        mock_authenticate.return_value = None

        with pytest.raises(exceptions.ValidationError):
            AuthService.loginService(mock_request)
