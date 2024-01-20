import pytest
from account.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def logined_client():
    client = APIClient()
    user = User.objects.create_user(
        login_id="kbs1115",
        email="bruce1115@naver.com",
        nickname="KKKBBBSSS",
        password="pwpwpwpw",
    )
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
