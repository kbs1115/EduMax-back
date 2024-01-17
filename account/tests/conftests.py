import pytest
from account.models import User


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
