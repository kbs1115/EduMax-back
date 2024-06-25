import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from community.domain.definition import POST_LIST_PAGE_SIZE
from community.tests.unit_tests.post_file_tests.conftests import *


class TestGetPostsApi:
    endpoint = reverse("community:posts")

    @pytest.mark.django_db
    def test_check_response_if_query_params_none(self, set_up_create_posts):
        client = APIClient()
        response = client.get(self.endpoint)

        assert response.status_code == 200

        data = response.json()

        assert data.get("message") == "post list successfully"
        page = data.get("data").get("page")
        page_size = data.get("data").get("page_size")
        list_size = data.get("data").get("list_size")
        post_list = data.get("data").get("post_list")
        assert page == 1
        assert page_size == POST_LIST_PAGE_SIZE
        assert list_size == 10
        assert post_list[0]["created_at"] >= post_list[1]["created_at"]
        assert post_list[0]["category"] == str(PostCategoriesParam.ENG_QUESTION)

    @pytest.mark.django_db
    def test_check_response_if_query_params_contain_page(self, set_up_create_posts):
        client = APIClient()
        response = client.get(self.endpoint, {"page": "2"})

        assert response.status_code == 200

        data = response.json()

        assert data.get("message") == "post list successfully"
        page = data.get("data").get("page")
        page_size = data.get("data").get("page_size")
        list_size = data.get("data").get("list_size")

        assert page == 2
        assert page_size == POST_LIST_PAGE_SIZE
        assert list_size == 10

    @pytest.mark.django_db
    def test_check_response_if_query_params_contain_search_filter_and_kw(
            self, set_up_create_posts
    ):
        client = APIClient()
        response = client.get(self.endpoint, {"search_filter": "TITLE", "q": "1"})
        assert response.status_code == 200

        data = response.json()
        assert data.get("message") == "post list successfully"
        page = data.get("data").get("page")
        page_size = data.get("data").get("page_size")
        list_size = data.get("data").get("list_size")
        post_list = data.get("data").get("post_list")
        assert page == 1
        assert page_size == POST_LIST_PAGE_SIZE
        # 1,10, 11, 12,13,14,15,16,17,18,19
        assert list_size == 10
        assert post_list[0]["created_at"] >= post_list[1]["created_at"]

    @pytest.mark.django_db
    def test_check_response_if_query_params_contain_search_filter_and_kw(
            self, set_up_create_posts
    ):
        client = APIClient()
        response = client.get(self.endpoint, {"search_filter": "TITLE", "q": "1"})
        assert response.status_code == 200

        data = response.json()
        assert data.get("message") == "post list successfully"
        page = data.get("data").get("page")
        page_size = data.get("data").get("page_size")
        list_size = data.get("data").get("list_size")

        assert page == 1
        assert page_size == POST_LIST_PAGE_SIZE
        # 1,10, 11, 12,13,14,15,16,17,18,19
        assert list_size == 10

    # like 만들어지면 like 순으로 정렬되는지 확인해야함
