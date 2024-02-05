import pytest
from rest_framework.test import APIClient
from community.tests.conftests import *


@pytest.mark.django_db(transaction=True)
class TestGetPostsApi:
    endpoint = 'posts/'

    def test_if_query_params_none(
            self,
            set_up_create_posts
    ):
        client = APIClient()
        response = client.get(self.endpoint)
        assert response
