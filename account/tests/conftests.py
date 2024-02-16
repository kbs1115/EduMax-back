import pytest
from django.core.mail import EmailMessage
from django.db.models import QuerySet
from rest_framework import status

from account.models import User, PwChangeTemporaryQueryParam, EmailTemporaryKey
from rest_framework.test import APIClient
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from account.service.email_service import EmailService
from account.service.user_service import UserService, SignUpService
from community.tests.unit_tests.post_file_tests.conftests import queryset_factory


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
def valid_EmailTemporaryKey_inst():
    return EmailTemporaryKey(email="dbsrbals26gmail.com", key="123456")


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


@pytest.fixture
def valid_data_for_RedirectPwChangeApiView():
    return {
        "email": "dbsrbals26@gmail.com",
        "auth_key": 123456
    }


@pytest.fixture
def invalid_data_for_RedirectPwChangeApiView():
    return {
        "email": "dbsrbals26@gmail.com",
        "auth_key": 1234567
    }


@pytest.fixture
def valid_data_for_DuplicateCheckerAPIView():
    return {
        "nickname": "dbsrbals2"
    }


@pytest.fixture
def invalid_data_for_DuplicateCheckerAPIView():
    return {
        "nickdxscname": "dbsrbals2"
    }


@pytest.fixture
def valid_data_for_EmailSenderApiView():
    return {
        "email": "dbsrbals26@gmail.com"
    }


@pytest.fixture
def invalid_data_for_EmailSenderApiView():
    return {
        "email": "dbsrbals26@gmaasdzxcasdzxd"
    }


@pytest.fixture
def mocked_EmailTemporaryKey_email_key_return_empty_query_set(mocker):
    empty_query_set = queryset_factory(EmailTemporaryKey)
    mocker = mocker.patch.object(EmailTemporaryKey.objects, "filter")
    mocker.return_value = empty_query_set
    return mocker


@pytest.fixture
def mocked_EmailTemporaryKey_orm_return_query_set(mocker, valid_EmailTemporaryKey_inst):
    query_set = queryset_factory(EmailTemporaryKey, [valid_EmailTemporaryKey_inst])
    mocker1 = mocker.patch.object(EmailTemporaryKey.objects, "filter")
    mocker2 = mocker.patch.object(QuerySet, "latest")
    mocker1.return_value = query_set
    mocker2.return_value = valid_EmailTemporaryKey_inst
    return [mocker1, mocker2, query_set]


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


@pytest.fixture
def mocked_method_make_random_query_param_with_email_auth(mocker):
    mocker = mocker.patch.object(UserService, "make_random_query_param_with_email_auth")
    mocker.return_value = "12345678"
    return mocker


@pytest.fixture
def mocked_method_get_user_with_email_auth(mocker, user_instance):
    mocker = mocker.patch.object(UserService, "get_user_with_email_auth")
    mocker.return_value = user_instance
    return mocker


@pytest.fixture
def mocked_method_check_duplicate_field_value(mocker):
    mocker = mocker.patch.object(SignUpService, "check_duplicate_field_value")
    mocker.return_value = True
    return mocker


@pytest.fixture
def mocked_method_check_authentication(mocker):
    mocker = mocker.patch("account.service.email_service.validate_email_key")
    mocker.return_value = True


@pytest.fixture
def mocked_method_create_password_change_param_model_inst_in_user_service(mocker):
    mocker.patch("account.service.user_service.create_password_change_param_model_inst")


@pytest.fixture
def mocked_method_delete_query_param_instance(mocker):
    mocker.patch("account.service.user_service.delete_query_param_instance")


@pytest.fixture
def mocked_method_send_email(mocker):
    mocker = mocker.patch.object(EmailService, "send_email")
    mocker.return_value = {"message": "email sent successfully", "status_code": status.HTTP_200_OK}
    return mocker


@pytest.fixture
def mocked_function_get_user_with_email(mocker, user_instance):
    mocker = mocker.patch("account.service.user_service.get_user_with_email")
    mocker.return_value = user_instance


@pytest.fixture
def mocked_function_create_email_key_model_instance_in_email_service(mocker, valid_EmailTemporaryKey_inst):
    mocker = mocker.patch("account.service.email_service.create_email_key_model_instance")
    mocker.return_value = valid_EmailTemporaryKey_inst

@pytest.fixture
def mocked_function_delete_email_key_instance_in_email_service(mocker):
    mocker.patch("account.service.email_service.delete_email_key_instance")


@pytest.fixture
def mocked_user_method(mocker):
    mocker.patch.object(User, "set_password")
    mocker.patch.object(User, "save")


@pytest.fixture
def mocked_smtp_email_send(mocker):
    mocker = mocker.patch.object(EmailMessage, "send")
    return mocker
