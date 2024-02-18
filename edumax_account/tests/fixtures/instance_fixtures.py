import pytest
from allauth.socialaccount.models import SocialAccount


@pytest.fixture
def social_account_instance(user_instance):
    social_account = SocialAccount(user=user_instance, uid="1", provider="google")
    return social_account
