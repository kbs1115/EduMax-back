import pytest
from account.tests.conftests import *
from account.service.user_service import *
from account.views import *
from unittest.mock import Mock
from rest_framework import exceptions
from rest_framework import status


class TestSignupView:
    def test_signup_with_invalid_data(self, mocker, invalid_request_data_wrong_email):
        mocker_create_user = mocker.patch.object(SignUpService, "create_user")
        mocker_create_user.side_effect = exceptions.ValidationError(
            "InvalidDataError_signup"
        )
        mock_request = Mock(data=invalid_request_data_wrong_email)

        with pytest.raises(exceptions.ValidationError):
            signup = UserAPIView()
            signup.post(mock_request)

    def test_signup_with_missing_data(self, mocker, invalid_request_data_omitted):
        mocker_create_user = mocker.patch.object(SignUpService, "create_user")
        mocker_create_user.side_effect = exceptions.ParseError(
            "InvalidDataError_signup"
        )
        mock_request = Mock(data=invalid_request_data_omitted)

        with pytest.raises(exceptions.ParseError):
            signup = UserAPIView()
            signup.post(mock_request)

    def test_signup_with_valid_data(self, mocker, valid_request_data):
        mocker_create_user = mocker.patch.object(SignUpService, "create_user")
        # mocking으로 valid_request_data를 그대로 반환한다고 가정한다. 실제로는 다른 정보도 더 들어 있음.
        mocker_create_user.return_value = valid_request_data
        mock_request = Mock(data=valid_request_data)

        signup = UserAPIView()
        actualResponse = signup.post(mock_request)
        actualData = actualResponse.data

        assert actualResponse.status_code == status.HTTP_200_OK
        assert actualData["user"] == valid_request_data
        assert actualData["message"] == "signup success"


# pk를 인자로 받는 경우와 받지 않는 경우가 있는데, 어짜피 service 단을 mocking할거라 하나의 class로 같이 테스트한다.
class TestUserView:
    def test_UserAPIView_get(self, mocker, valid_user_data, user_instance):
        mocker_create_user = mocker.patch.object(UserService, "get_serializer_data")
        mocker_create_user.return_value = valid_user_data
        mock_request = Mock(user=user_instance)

        api = UserAPIView()
        res = api.get(mock_request)

        assert res.data == valid_user_data
        assert res.status_code == 200

    def test_UserAPIView_patch(
        self,
        mocker,
        valid_user_data,
        user_instance,
        valid_patch_data,
        invalid_patch_data,
    ):
        mocker_create_user = mocker.patch.object(UserService, "update_user")
        mocker_create_user.return_value = valid_user_data
        mock_request = Mock(user=user_instance, data=valid_patch_data)

        api = UserAPIView()
        res = api.patch(mock_request)

        assert res.data == valid_user_data
        assert res.status_code == 200

        mock_request = Mock(user=user_instance, data={"nickname": "KKBBBS"})
        res = api.patch(mock_request)
        assert res.status_code == 200

        with pytest.raises(exceptions.ParseError):
            mock_request = Mock(user=user_instance, data=invalid_patch_data)
            res = api.patch(mock_request)

        with pytest.raises(exceptions.ParseError):
            mock_request = Mock(user=user_instance, data={})
            res = api.patch(mock_request)

    def test_UserAPIView_delete(self, mocker, valid_user_data, user_instance):
        mocker_create_user = mocker.patch.object(UserService, "delete_user")
        mocker_create_user.return_value = valid_user_data
        mock_request = Mock(user=user_instance)

        api = UserAPIView()
        res = api.delete(mock_request)

        assert res.data == {}
        assert res.status_code == 204


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
        mocker_loginService.side_effect = exceptions.ValidationError("InvalidUserError")
        mock_request = Mock(data=invalid_login_data)

        with pytest.raises(exceptions.ValidationError):
            login = AuthAPIView()
            login.post(mock_request)

    def test_login_with_strange_key(self, mocker, invalid_login_data_with_strange_key):
        mocker_loginService = mocker.patch.object(AuthService, "loginService")
        mocker_loginService.side_effect = exceptions.ValidationError("InvalidUserError")
        mock_request = Mock(data=invalid_login_data_with_strange_key)

        with pytest.raises(exceptions.ParseError):
            login = AuthAPIView()
            login.post(mock_request)
