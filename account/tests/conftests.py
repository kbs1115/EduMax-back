import pytest
from account.models import User, PwChangeTemporaryQueryParam
from rest_framework.test import APIClient
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from account.service.user_service import UserService


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def logined_client():
    client = APIClient()
    user = User(
        id=1,
        login_id="kbs1115",
        email="bruce1115@naver.com",
        nickname="KKKBBBSSS",
        password="pwpwpwpw",
    )
    user.save()
    user2 = User(id=2)
    user2.save()
    token = TokenObtainPairSerializer.get_token(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")

    return client


@pytest.fixture
def valid_request_data():
    return {
        "login_id": "bruce1118",
        "email": "bruce1118@naver.com",
        "nickname": "KBS3",
        "password": "Bb3848948389!!!",
    }


@pytest.fixture
def invalid_request_data_omitted():
    return {
        "email": "bruce1118@naver.com",
        "nickname": "KBS3",
        "password": "Bb3848948389!!!",
    }


@pytest.fixture
def invalid_request_data_wrong_email():
    return {
        "login_id": "bruce1118",
        "email": "bruce1118naver.com",
        "nickname": "KBS3",
        "password": "Bb3848948389!!!",
    }


@pytest.fixture
def valid_login_data():
    return {
        "login_id": "bruce1118",
        "password": "Bb3848948389!!!",
    }


@pytest.fixture
def invalid_login_data():
    return {
        "login_id": "bruce1119",
        "password": "Bb3848948389!!!",
    }


@pytest.fixture
def invalid_login_data_with_strange_key():
    return {
        "bbb": "bruce1119121",
        "password": "Bb3848948389!!!",
    }


@pytest.fixture
def user_instance():
    user = User(
        id=1,
        login_id="kbs1115",
        email="bruce1115@naver.com",
        nickname="KKKBBBSSS",
        password="pwpwpwpw",
    )
    return user


@pytest.fixture
def valid_serialized_data():
    return {
        "login_id": "kbs1115",
        "email": "bruce1115@naver.com",
        "nickname": "KKKBBBSSS",
        "password": "pwpwpwpw",
    }


@pytest.fixture
def invalid_serialized_data():
    return {
        "login_id": "kbs1115121739479178937491873894789193yyyyyyyy",
        "email": "bruce1115@naver.com",
        "nickname": "KKKBBBSSS",
        "password": "pwpwpwpw",
    }


@pytest.fixture
def valid_user_data():
    return {
        "login_id": "kbs1115",
        "email": "bruce1115@naver.com",
        "nickname": "KKKBBBSSS",
    }


@pytest.fixture
def valid_patch_data():
    return {
        "email": "bruce1116@naver.com",
        "nickname": "KKKBBBSSS",
    }


@pytest.fixture
def invalid_patch_data():
    return {
        "emaile": "bruce1116@naver.com",
    }


@pytest.fixture
def valid_data_for_password_change_api_view():
    return [
        {
            "verify": "123123"
        },
        {
            "new_pw": "dbsrbals12",
            "email": "dbsrbals26@gmail.com"
        }
    ]

@pytest.fixture
def invalid_data_for_password_change_api_view():
    return [
        {
            "verify": "123123"
        },
        {
            "new_pw": "dbsrbals12",
            "email": "dbsrbals26asd654ds465as654"
        }
    ]



def valid_data_for_RedirectPwChangeApiView():
    return {
        "email": "dbsrbals26@gmail.com",
        "auth_key": 123456
    }


def invalid_data_for_RedirectPwChangeApiView():
    return {
        "email": "dbsrbals26@gmail.com",
        "auth_key": 1234567
    }


@pytest.fixture
def mocked_user_access(mocker):
    mocker.patch("account.model.user_access")


@pytest.fixture
def mocked_check_pw_change_page_query_param(mocker):
    mocker = mocker.patch("account.model.user_access.check_pw_change_page_query_param")
    return mocker


@pytest.fixture
def mocked_method_change_password(mocker):
    mocker = mocker.patch.object(UserService, "change_password")
    return mocker
