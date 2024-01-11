import pytest
from pytest_drf import (
    UsesDeleteMethod,
    UsesDetailEndpoint,
    UsesPostMethod,
    APIViewTest,
)
from pytest_lambda import lambda_fixture
from django.urls import reverse


# class TestSignup(APIViewTest, UsesPostMethod):
#     url = lambda_fixture(lambda: reverse("signup"))

#     def test_signup_with_valid_data(self):
