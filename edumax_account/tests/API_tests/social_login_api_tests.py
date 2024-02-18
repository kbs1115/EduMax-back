import pytest
from django.urls import reverse

from edumax_account.view.social_login_views import *
from edumax_account.models import User

load_dotenv(verbose=True)
BASE_URL = "http://localhost:8000/"
GOOGLE_CALLBACK_URI = BASE_URL + "auth/user/google/redirection/"


class TestSocialLoginAPI:
    client_id = os.environ.get("SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("SOCIAL_AUTH_GOOGLE_SECRET")

    # 적절한 위치로 redirection이 되는지 확인한다.
    def test_google_oauth_redirect(self, client):
        endpoint = reverse("edumax_account:google_login")
        scope = "https://www.googleapis.com/auth/userinfo.email"
        client_id = os.getenv("SOCIAL_AUTH_GOOGLE_CLIENT_ID")

        res = client.get(endpoint)

        assert (
            res["Location"]
            == f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}"
        )

    @pytest.mark.django_db
    def test_google_callback(
        self,
        client,
        mocked_social_callback,
    ):
        endpoint = reverse("edumax_account:google_callback") + "?code=codecode"

        res = client.get(endpoint)

        user = User.objects.get(email="test@naver.com")
        social_account = SocialAccount.objects.get(user=user)

        mocked_post = mocked_social_callback[0]
        mocked_get = mocked_social_callback[1]

        mocked_post.assert_any_call(
            "https://oauth2.googleapis.com/token",
            data={
                "code": "codecode",  # 유효한 코드
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "authorization_code",
                "redirect_uri": GOOGLE_CALLBACK_URI,
            },
        )
        mocked_post.assert_any_call(
            f"https://oauth2.googleapis.com/revoke", data={"token": "accesstokentest"}
        )
        mocked_get.assert_any_call(
            f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=accesstokentest"
        )
        assert res.status_code == 200
        assert res.data["message"] == "Signup and login success"
        assert res.data["user"]["nickname"] == user.nickname
        assert social_account.uid == "1"

        res = client.get(endpoint)
        assert res.status_code == 200
        assert res.data["message"] == "login success"
