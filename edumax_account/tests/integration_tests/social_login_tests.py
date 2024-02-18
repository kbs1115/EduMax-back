import pytest
from allauth.socialaccount.models import SocialAccount

from edumax_account.models import User
from edumax_account.service.user_service import SignUpService, UserService, AuthService


class TestSocialLoginService:
    # create_social_user를 DB, Serializer와 묶어서 생성한다.
    @pytest.mark.django_db
    def test_create_social_user(self):
        user = SignUpService.create_social_user("test@naver.com")
        user_inst = User.objects.get(email="test@naver.com")

        assert len(user_inst.login_id) == 8
        assert len(user_inst.nickname) == 6

        social_account_inst = SocialAccount.objects.get(user=user_inst)

        assert social_account_inst.uid == "1"
        assert social_account_inst.provider == "google"

    # user로 바로 로그인할 수 있도록 함.
    def test_social_login_service(self, user_instance):
        data = AuthService.social_login_service(user_instance)

        assert data["refreshToken"]
        assert data["accessToken"]
        assert data["userData"]["nickname"] == user_instance.nickname
