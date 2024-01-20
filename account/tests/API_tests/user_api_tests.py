import pytest
from account.tests.conftests import *
from django.urls import reverse
from account.services import *
from account.views import *
from rest_framework.request import Request

{"code": 404, "errors": "user not found"}


# 자신의 User 정보와 회원가입에 대한 API
class TestUserAPI:
    endpoint = reverse("account:user")

    @pytest.mark.django_db
    def test_get_my_data(self, logined_client, valid_user_data):
        res = logined_client.get(self.endpoint)

        assert res.data == valid_user_data
        assert res.status_code == 200

    @pytest.mark.django_db
    def test_get_my_data_unauthenticated(self, client):
        res = client.get(self.endpoint)

        assert res.data == {
            "code": 401,
            "errors": "Authentication credentials were not provided.",
        }
        assert res.status_code == 401
