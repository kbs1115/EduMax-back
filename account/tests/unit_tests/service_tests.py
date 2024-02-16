from account.serializers import UserSerializer
from account.service.user_service import SignUpService, UserService, AuthService
from account.tests.conftests import *
from account.view.user_views import *
from account.models import User
from unittest.mock import Mock, patch
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

        result = SignUpService().create_user(mock_request.data)

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
            SignUpService().create_user(mock_request)

    def test_signup_with_wrong_email_user_data(
            self, invalid_request_data_wrong_email, mocker
    ):
        mock_request = Mock(data=invalid_request_data_wrong_email)
        mock_save = mocker.patch.object(UserSerializer, "save")
        mocker.patch.object(
            UniqueValidator, "__call__"
        )  # unique 조건을 test하는 Validator의 __call__ method를 mocking한다.

        with pytest.raises(exceptions.ValidationError):
            SignUpService().create_user(mock_request)

    def test_duplicate_check_if_field_duplicate(self):
        pass

    def test_duplicate_check_if_field_not_duplicate(self):
        pass


class TestUserService:
    mock_request = Mock()
    mock_view = Mock()

    # get_user에 관련된 함수를 한번에 테스트
    def test_get_serializer_data(self, user_instance):
        data = UserService.get_serializer_data(user_instance)

        assert data == {
            "login_id": "kbs1115",
            "email": "bruce1115@naver.com",
            "nickname": "KKKBBBSSS",
        }

    def test_update_user_with_valid_data(self, mocker, user_instance):
        mock_request = Mock(data={"email": "abcdetest123@naver.com"})
        mocker.patch.object(UniqueValidator, "__call__")
        mock_save = mocker.patch.object(User, "save")

        data = UserService.update_user(user_instance, mock_request.data)

        mock_save.assert_called_once()
        assert data == {
            "login_id": "kbs1115",
            "email": "abcdetest123@naver.com",
            "nickname": "KKKBBBSSS",
        }

    def test_update_user_with_invalid_data(self, mocker, user_instance):
        mock_request = Mock(data={"email": "abcdetest123naver.com"})
        mocker.patch.object(UniqueValidator, "__call__")
        mock_save = mocker.patch.object(User, "save")

        with pytest.raises(exceptions.ValidationError):
            data = UserService.update_user(user_instance, mock_request.data)

    def test_delete_user(self, mocker, user_instance):
        mock_request = Mock()
        mock_delete = mocker.patch.object(User, "delete")

        UserService.delete_user(user_instance)

        mock_delete.assert_called_once()

    def test_delete_invalid_user(self, mocker, user_instance):
        mock_request = Mock()
        mock_delete = mocker.patch.object(User, "delete")
        mock_delete.side_effect = Exception()

    def test_method_generate_random_string(self):
        random_string = UserService.generate_random_string()
        assert len(random_string) == 8

    def test_method_get_user_with_email_auth_assert_called(
            self,
            mocked_function_get_user_with_email,
            mocked_method_check_authentication,
            user_instance

    ):
        response = UserService.get_user_with_email_auth(
            email="dbsrbals26@gmail.com",
            auth_key="123456"
        )
        assert response == user_instance

    def test_method_make_random_query_param_with_email_auth_assert_called(
            self,
            mocked_method_check_authentication,
            mocked_method_create_password_change_param_model_inst,
            mocked_method_delete_query_param_instance
    ):
        with patch("django.db.transaction.atomic"):
            response = UserService().make_random_query_param_with_email_auth(
                email="dbsrbals26@gmail.com",
                auth_key="123456"
            )
            assert len(response) == 8

    def test_method_change_password_assert_called(
            self,
            mocked_function_get_user_with_email,
            mocked_user_method
    ):
        with patch("django.db.transaction.atomic"):
            UserService().change_password(pw="123", email="dbsrbals26@gmail.com")


class TestAuthService:
    def test_valid_login(self, valid_login_data, mocker):
        mock_request = Mock(data=valid_login_data)
        mock_authenticate = mocker.patch("account.service.user_service.authenticate")
        mock_authenticate.return_value = User(id=1)
        serializer = UserSerializer(mock_authenticate.return_value)

        actual = AuthService().loginService(mock_request)

        assert mock_authenticate.is_called_once()

        # 각 데이터가 제대로 들어왔는지 존재 여부를 확인한다.(token은 random이므로 정확히 비교하는 것은 옳지 않다.)
        assert actual["userData"] == serializer.data
        assert "accessToken" in actual
        assert "refreshToken" in actual

    def test_invalid_login(self, invalid_login_data, mocker):
        mock_request = Mock(data=invalid_login_data)
        mock_authenticate = mocker.patch("account.service.user_service.authenticate")
        mock_authenticate.return_value = None

        with pytest.raises(exceptions.ValidationError):
            AuthService().loginService(mock_request)


class TestEmailService:
    def test_method_check_authentication_assert_called(self):
        pass

    def test_method_send_email_assert_called(self):
        pass

    def test_method_generate_random_number(self):
        pass
