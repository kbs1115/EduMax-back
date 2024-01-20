import pytest
from account.tests.conftests import *
from django.urls import reverse
from account.services import *
from account.views import *
from django.core.exceptions import ObjectDoesNotExist


# 자신의 User 정보와 회원가입에 대한 API
class TestUserAPI:
    endpoint = reverse("account:user")

    @pytest.mark.django_db
    def test_get_my_data(self, logined_client, valid_user_data):
        res = logined_client.get(self.endpoint)

        assert res.data == valid_user_data
        assert res.status_code == 200

    @pytest.mark.django_db
    def test_get_my_data_not_authenticated(self, client):
        res = client.get(self.endpoint)

        assert res.data == {
            "code": 401,
            "errors": "Authentication credentials were not provided.",
        }
        assert res.status_code == 401

    @pytest.mark.django_db
    def test_patch_my_data(self, logined_client):
        res = logined_client.patch(
            self.endpoint, {"email": "abcdetest123@naver.com"}, format="json"
        )

        assert res.data == {
            "login_id": "kbs1115",
            "email": "abcdetest123@naver.com",
            "nickname": "KKKBBBSSS",
        }
        assert res.status_code == 200

    @pytest.mark.django_db
    def test_patch_my_data_invalid_data(self, logined_client):
        res1 = logined_client.patch(
            self.endpoint, {"emai": "abcdetest123@naver.com"}, format="json"
        )

        assert res1.status_code == 400  # ValidationError

        res2 = logined_client.patch(
            self.endpoint, {"email": "abcdetest123naver.com"}, format="json"
        )

        assert res2.status_code == 400  # ValidationError

    @pytest.mark.django_db
    def test_delete_my_data(self, logined_client):
        assert User.objects.filter(login_id="kbs1115").exists()

        res = logined_client.delete(self.endpoint)

        assert res.status_code == status.HTTP_204_NO_CONTENT
        assert not User.objects.filter(login_id="kbs1115").exists()


class TestCertainUserAPI:
    # 접속 user의 id는 1이다.
    # Permission과 Authentication은 APIView가 공유하므로 GET 하나로 테스트
    @pytest.mark.django_db
    def test_get_my_data(self, logined_client, valid_user_data):
        endpoint = reverse("account:certainUser", kwargs={"pk": 1})
        res = logined_client.get(endpoint)

        assert res.data == valid_user_data
        assert res.status_code == 200

    @pytest.mark.django_db
    def test_get_my_data_permission_denied(self, logined_client):
        endpoint = reverse("account:certainUser", kwargs={"pk": 2})
        res = logined_client.get(endpoint)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_get_my_data_not_authenticated(self, client):
        endpoint = reverse("account:certainUser", kwargs={"pk": 1})
        res = client.get(endpoint)

        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_patch_my_data(self, logined_client):
        endpoint = reverse("account:certainUser", kwargs={"pk": 1})
        res = logined_client.patch(
            endpoint, {"email": "abcdetest123@naver.com"}, format="json"
        )

        assert res.data == {
            "login_id": "kbs1115",
            "email": "abcdetest123@naver.com",
            "nickname": "KKKBBBSSS",
        }
        assert res.status_code == 200

    @pytest.mark.django_db
    def test_patch_my_data_invalid_data(self, logined_client):
        endpoint = reverse("account:certainUser", kwargs={"pk": 1})
        res1 = logined_client.patch(
            endpoint, {"emai": "abcdetest123@naver.com"}, format="json"
        )

        assert res1.status_code == 400  # ValidationError

        res2 = logined_client.patch(
            endpoint, {"email": "abcdetest123naver.com"}, format="json"
        )

        assert res2.status_code == 400  # ValidationError

    @pytest.mark.django_db
    def test_delete_my_data(self, logined_client):
        endpoint = reverse("account:certainUser", kwargs={"pk": 1})
        assert User.objects.filter(login_id="kbs1115").exists()

        res = logined_client.delete(endpoint)

        assert res.status_code == status.HTTP_204_NO_CONTENT
        assert not User.objects.filter(login_id="kbs1115").exists()
