import pytest


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


@pytest.fixture
def valid_login_data():
    # 유효하지 않은 request 데이터를 반환한다.
    return {
        "login_id": "bruce1118",
        "password": "Bb3848948389!!!",
    }


@pytest.fixture
def invalid_login_data():
    # 유효하지 않은 request 데이터를 반환한다.
    return {
        "login_id": "bruce1119",
        "password": "Bb3848948389!!!",
    }


@pytest.fixture
def invalid_login_data_with_strange_key():
    # 유효하지 않은 request 데이터를 반환한다.
    return {
        "bbb": "bruce1119121",
        "password": "Bb3848948389!!!",
    }
