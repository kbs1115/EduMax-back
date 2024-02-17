from rest_framework.parsers import MultiPartParser
from rest_framework.templatetags import rest_framework

from edumax_account.service.user_service import SignUpService, UserService, AuthService
from edumax_account.tests.conftests import *
from edumax_account.view.email_views import EmailSenderApiView
from edumax_account.view.user_views import *
from unittest.mock import Mock
from rest_framework import exceptions
from rest_framework import status
from rest_framework.request import Request
from edumax_account.view.user_views import UserAPIView, AuthAPIView
from rest_framework.test import APIRequestFactory


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


class TestPasswordChangeApiView:
    view_path = "auth/user/pw-change/"

    def test_assert_called(
        self,
        mocked_check_pw_change_page_query_param,
        valid_data_for_password_change_api_view,
        mocked_method_change_password,
    ):
        """
        valid 데이터를 넘겨줬을때 모든 메소드가 적절히 호출되는지 확인
        """

        value = valid_data_for_password_change_api_view[0]["verify"]
        body = valid_data_for_password_change_api_view[1]
        path = self.view_path + f"?verify={value}"
        factory = APIRequestFactory()
        request = factory.post(path, data=body)
        request = Request(request, parsers=[MultiPartParser()])
        response = PasswordChangeApiView().post(request)
        mocked_check_pw_change_page_query_param.assert_called_once()
        mocked_method_change_password.assert_called_once()
        assert response

    def test_invalid_body_data(
        self,
        mocked_check_pw_change_page_query_param,
        invalid_data_for_password_change_api_view,
        mocked_method_change_password,
    ):
        """
        조건에 맞지않는 body_data가 입력됬을때 validator에서
        거를수있는지 확인
        """
        value = invalid_data_for_password_change_api_view[0]["verify"]
        body = invalid_data_for_password_change_api_view[1]
        path = self.view_path + f"?verify={value}"
        factory = APIRequestFactory()
        request = factory.post(path, data=body)
        request = Request(request, parsers=[MultiPartParser()])

        with pytest.raises(exceptions.ParseError):
            PasswordChangeApiView().post(request)
            mocked_check_pw_change_page_query_param.assert_called_once()


class TestRedirectPwChangeApiView:
    view_path = "user/pw-change/email-auth/"

    def test_assert_called(
        self,
        mocked_method_make_random_query_param_with_email_auth,
        valid_data_for_RedirectPwChangeApiView,
    ):
        """
        valid 데이터를 넘겨줬을때 모든 메소드가 적절히 호출되는지 확인
        """

        factory = APIRequestFactory()
        request = factory.post(
            self.view_path, data=valid_data_for_RedirectPwChangeApiView
        )
        request = Request(request, parsers=[MultiPartParser()])
        response = RedirectPwChangeApiView().post(request)
        mocked_method_make_random_query_param_with_email_auth.assert_called_once()
        assert response
        url = response.data["data"]["redirect_url"]
        assert url == "user/pw-change/?verify=12345678"

    def test_invalid_body_data(
        self,
        mocked_method_make_random_query_param_with_email_auth,
        invalid_data_for_RedirectPwChangeApiView,
    ):
        """
        invalid 데이터를 넘겨줬을때 예외를 잡는지
        """

        factory = APIRequestFactory()
        request = factory.post(
            self.view_path, data=invalid_data_for_RedirectPwChangeApiView
        )
        request = Request(request, parsers=[MultiPartParser()])
        with pytest.raises(exceptions.ParseError):
            RedirectPwChangeApiView().post(request)


class TestGetLoginIdApiView:
    view_path = "user/id-find/email-auth/"

    def test_assert_called(
        self,
        mocked_method_get_user_with_email_auth,
        valid_data_for_RedirectPwChangeApiView,
    ):
        """
        valid 데이터를 넘겨줬을때 모든 메소드가 적절히 호출되는지 확인
        """

        factory = APIRequestFactory()
        request = factory.post(
            self.view_path, data=valid_data_for_RedirectPwChangeApiView
        )
        request = Request(request, parsers=[MultiPartParser()])
        response = GetLoginIdApiView().post(request)
        mocked_method_get_user_with_email_auth.assert_called_once()
        assert response

    def test_invalid_body_data(
        self,
        mocked_method_get_user_with_email_auth,
        invalid_data_for_RedirectPwChangeApiView,
    ):
        """
        invalid 데이터를 넘겨줬을때 예외를 잡는지
        """

        factory = APIRequestFactory()
        request = factory.post(
            self.view_path, data=invalid_data_for_RedirectPwChangeApiView
        )
        request = Request(request, parsers=[MultiPartParser()])
        with pytest.raises(exceptions.ParseError):
            GetLoginIdApiView().post(request)


class TestDuplicateCheckerAPIView:
    view_path = "user/duplicate-check/"

    def test_assert_called(
        self,
        mocked_method_check_duplicate_field_value,
        valid_data_for_RedirectPwChangeApiView,
    ):
        """
        valid 데이터를 넘겨줬을때 모든 메소드가 적절히 호출되는지 확인
        """

        factory = APIRequestFactory()
        request = factory.post(
            self.view_path, data=valid_data_for_RedirectPwChangeApiView
        )
        request = Request(request, parsers=[MultiPartParser()])
        response = DuplicateCheckerAPIView().post(request)
        mocked_method_check_duplicate_field_value.assert_called_once()
        assert response.data["message"] == "duplicate"

    def test_invalid_body_data(
        self,
        mocked_method_check_duplicate_field_value,
        invalid_data_for_DuplicateCheckerAPIView,
    ):
        """
        invalid 데이터를 넘겨줬을때 예외를 잡는지
        """

        factory = APIRequestFactory()
        request = factory.post(
            self.view_path, data=invalid_data_for_DuplicateCheckerAPIView
        )
        request = Request(request, parsers=[MultiPartParser()])
        with pytest.raises(exceptions.ParseError):
            GetLoginIdApiView().post(request)


class TestEmailSenderApiView:
    view_path = "user/duplicate-check/"

    def test_assert_called(
        self,
        mocked_method_send_email,
        valid_data_for_EmailSenderApiView,
    ):
        """
        valid 데이터를 넘겨줬을때 모든 메소드가 적절히 호출되는지 확인
        """

        factory = APIRequestFactory()
        request = factory.post(self.view_path, data=valid_data_for_EmailSenderApiView)
        request = Request(request, parsers=[MultiPartParser()])
        response = EmailSenderApiView().post(request)
        mocked_method_send_email.assert_called_once()
        assert response

    def test_invalid_body_data(
        self,
        mocked_method_check_duplicate_field_value,
        invalid_data_for_EmailSenderApiView,
    ):
        """
        invalid 데이터를 넘겨줬을때 예외를 잡는지
        """

        factory = APIRequestFactory()
        request = factory.post(self.view_path, data=invalid_data_for_EmailSenderApiView)
        request = Request(request, parsers=[MultiPartParser()])
        with pytest.raises(exceptions.ParseError):
            EmailSenderApiView().post(request)
