import pytest
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator

from edumax_account.service.user_service import *

USER_SERVICE_LOCATION = "edumax_account.service.user_service"
SOCIAL_LOGIN_VIEW_LOCATION = "edumax_account.view.social_login_views."


@pytest.fixture
def mocked_user_serializer_save(mocker):
    mocker.patch.object(UniqueValidator, "__call__")
    return mocker.patch.object(UserSerializer, "save")


@pytest.fixture
def mocked_social_account_create_serializer_save(mocker):
    mocker.patch.object(UniqueValidator, "__call__")
    return mocker.patch.object(SocialAccountCreateSerializer, "save")


@pytest.fixture
def mocked_redirect(mocker):
    return mocker.patch(SOCIAL_LOGIN_VIEW_LOCATION + "redirect")


@pytest.fixture
def mocked_social_callback(mocker):
    mocked_res1 = mocker.Mock()
    mocked_res1.json.return_value = {"access_token": "accesstokentest"}
    mocked_res2 = mocker.Mock(status_code=200)
    mocked_res2.json.return_value = {"email": "test@naver.com"}

    # 함수의 인자에 따라 다른 반환값을 제공하는 함수 생성
    def custom_post_side_effect(*args, **kwargs):
        if args[0] == "https://oauth2.googleapis.com/token":
            return mocked_res1
        else:
            return Response({}, status=200)

    def custom_get_side_effect(*args, **kwargs):
        return mocked_res2

    mocked_post = mocker.patch(SOCIAL_LOGIN_VIEW_LOCATION + "requests.post")
    mocked_get = mocker.patch(SOCIAL_LOGIN_VIEW_LOCATION + "requests.get")

    mocked_post.side_effect = custom_post_side_effect
    mocked_get.side_effect = custom_get_side_effect

    return [mocked_post, mocked_get]


@pytest.fixture
def mocked_get_user_with_email(mocker, user_instance):
    mocked_func = mocker.patch(SOCIAL_LOGIN_VIEW_LOCATION + "get_user_with_email")
    mocked_func.return_value = user_instance
    return mocked_func


@pytest.fixture
def mocked_get_social_user_with_user(mocker):
    return mocker.patch(SOCIAL_LOGIN_VIEW_LOCATION + "get_social_user_with_user")


@pytest.fixture
def mocked_social_login_service(mocker, user_instance):
    mocked_func = mocker.patch.object(AuthService, "social_login_service")
    mocked_func.return_value = {
        "accessToken": "accessTest",
        "refreshToken": "refreshTest",
        "userData": user_instance.nickname,
    }
    return mocked_func
