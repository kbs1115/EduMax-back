import pytest
from account.tests.conftests import *
from account.services import *
from account.views import *
from unittest.mock import Mock
from rest_framework import exceptions
from rest_framework import status


class TestSignupView:
    def test_signup_with_invalid_data(self, mocker, invalid_request_data_wrong_email):
        mocker_get_user_data = mocker.patch.object(SignUpService, "get_user_data")
        mocker_get_user_data.side_effect = exceptions.ParseError(
            "InvalidDataError_signup"
        )
        mock_request = Mock(data=invalid_request_data_wrong_email)

        with pytest.raises(exceptions.ParseError):
            signup = SignUpAPIView()
            signup.post(mock_request)

    def test_signup_with_valid_data(self, mocker, valid_request_data):
        mocker_get_user_data = mocker.patch.object(SignUpService, "get_user_data")
        # mocking으로 valid_request_data를 그대로 반환한다고 가정한다. 실제로는 다른 정보도 더 들어 있음.
        mocker_get_user_data.return_value = valid_request_data
        mock_request = Mock(data=valid_request_data)

        signup = SignUpAPIView()
        actualResponse = signup.post(mock_request)
        actualData = actualResponse.data

        assert actualResponse.status_code == status.HTTP_200_OK
        assert actualData["user"] == valid_request_data
        assert actualData["message"] == "signup success"


class TestAuthView:
    # set_cookie의 test는 integration test에서 api를 테스트할 때 진행한다.
    def test_login_with_valid_data(self, mocker, valid_login_data):
        mocker_loginService = mocker.patch.object(AuthService, "loginService")
        mocker_loginService.return_value = {
            "userData": valid_login_data,
            "refreshToken": "testrefreshToken",
            "accessToken": "testaccessToken",
        }
        mock_request = Mock(data=valid_login_data)

        login = AuthAPIView()
        actualResponse = login.post(mock_request)
        actualData = actualResponse.data

        # status code와 response의 data 값을 확인한다.
        assert actualResponse.status_code == status.HTTP_200_OK
        assert actualData["user"] == valid_login_data
        assert actualData["message"] == "login success"
        assert actualData["token"] == {
            "refresh": "testrefreshToken",
            "access": "testaccessToken",
        }

    def test_login_with_invalid_data(self, mocker, invalid_login_data):
        mocker_loginService = mocker.patch.object(AuthService, "loginService")
        mocker_loginService.side_effect = exceptions.ParseError("InvalidUserError")
        mock_request = Mock(data=invalid_login_data)

        with pytest.raises(exceptions.ParseError):
            login = AuthAPIView()
            login.post(mock_request)
