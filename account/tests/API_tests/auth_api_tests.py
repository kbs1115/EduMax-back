import pytest
from account.tests.conftests import *
from django.urls import reverse


class TestLoginAPI:
    endpoint = reverse("account:token")

    def test_login(self, client, user_instance, mocker):
        mock_authenticate = mocker.patch("account.services.authenticate")
        mock_authenticate.return_value = user_instance

        response = client.post(
            self.endpoint,
            {"login_id": "kbs1115", "password": "pwpwpwpw"},
            format="json",
        )
        body = response.data
        token = body["token"]

        assert body["user"].get("login_id") == user_instance.login_id
        assert body["message"] == "login success"
        assert token.get("access") is not None
        assert token.get("refresh") is not None

    def test_invalid_login_with_strange_key(
        self, client, invalid_login_data_with_strange_key
    ):
        response = client.post(
            self.endpoint,
            invalid_login_data_with_strange_key,
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == 400
        assert response.data["errors"] == "invalid data form"

    def test_invalid_login_with_invalid_user(self, client, invalid_login_data, mocker):
        mock_authenticate = mocker.patch("account.services.authenticate")
        mock_authenticate.return_value = None

        response = client.post(
            self.endpoint,
            invalid_login_data,
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == 400
        assert response.data["errors"] == [
            "The provided information does not match any user."
        ]
