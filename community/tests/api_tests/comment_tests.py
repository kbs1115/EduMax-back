import pytest
from django.urls import reverse

from community.tests.api_tests.conftests import *


class TestMakeCommentToPostAPI:
    @pytest.mark.django_db
    def test_create_comment(self, client, logined_client, setup_data):
        endpoint = reverse("community:post_comment", kwargs={"post_id": 2})

        # 로그인된 유저 테스트
        response = logined_client[0].post(
            endpoint,
            {"content": "testcontent3", "html_content": "htmltestcontent3"},
            format="json",
        )

        assert response.status_code == 201
        assert response.data["data"]["post_id"] == 2
        assert response.data["data"]["author"] == setup_data[4].login_id
        assert Comment.objects.get(post_id=2)

        # 로그인 안 된 유저 테스트
        response = client.post(
            endpoint,
            {"content": "testcontent3", "html_content": "htmltestcontent3"},
            format="json",
        )

        assert response.status_code == 401


class TestCommentAPI:
    @pytest.mark.django_db
    def test_retrieve_comment(self, client, logined_client, setup_data):
        endpoint = reverse("community:comment", kwargs={"comment_id": 1})

        # 로그인 사용자에 대한 테스트
        response = logined_client[0].get(endpoint)

        assert response.status_code == 200
        assert response.data["message"] == "Comment retrieve successfully"
        assert response.data["data"]["content"] == setup_data[2].content
        assert response.data["data"]["author"] == setup_data[2].author.nickname

        # 비로그인 사용자에 대한 테스트
        response = client.get(endpoint)

        assert response.status_code == 200
        assert response.data["message"] == "Comment retrieve successfully"
        assert response.data["data"]["content"] == setup_data[2].content
        assert response.data["data"]["author"] == setup_data[2].author.nickname

    @pytest.mark.django_db
    def test_create_comment(self, client, logined_client, setup_data):
        endpoint = reverse("community:comment", kwargs={"comment_id": 1})

        # 로그인된 유저 테스트
        response = logined_client[0].post(
            endpoint,
            {"content": "testcontent3", "html_content": "htmltestcontent3"},
            format="json",
        )

        assert response.status_code == 201
        assert response.data["data"]["post_id"] == setup_data[0].id
        assert response.data["data"]["author"] == setup_data[4].login_id
        assert Comment.objects.all().count() == 3

        # 로그인 안 된 유저 테스트
        response = client.post(
            endpoint,
            {"content": "testcontent3", "html_content": "htmltestcontent3"},
            format="json",
        )

        assert response.status_code == 401

    @pytest.mark.django_db
    def test_update_comment(self, client, logined_client, setup_data):
        endpoint = reverse("community:comment", kwargs={"comment_id": 2})

        # 로그인된 유저 테스트(자신의 댓글)
        response = logined_client[0].patch(
            endpoint,
            {
                "content": "testcontent_updated",
                "html_content": "htmltestcontent_updated",
                "files_state": "DELETE",
            },
            format="json",
        )

        assert response.status_code == 200
        assert response.data["data"]["post_id"] == setup_data[0].id
        assert response.data["data"]["author"] == setup_data[4].login_id
        assert Comment.objects.get(id=2).content == "testcontent_updated"

        # 로그인된 유저 테스트(자신의 댓글) - File state wrong
        response = logined_client[0].patch(
            endpoint,
            {
                "content": "testcontent_updated",
                "html_content": "htmltestcontent_updated",
                "files_state": "eeee",
            },
            format="json",
        )

        assert response.status_code == 400

        # 로그인된 유저 테스트(자신의 댓글이 아님)
        response = logined_client[1].patch(
            endpoint,
            {
                "content": "testcontent_updated",
                "html_content": "htmltestcontent_updated",
                "files_state": "DELETE",
            },
            format="json",
        )

        assert response.status_code == 403

        # 로그인 안 된 유저 테스트
        response = client.patch(
            endpoint,
            {
                "content": "testcontent_updated",
                "html_content": "htmltestcontent_updated",
                "files_state": "DELETE",
            },
            format="json",
        )

        assert response.status_code == 401

    @pytest.mark.django_db
    def test_delete_comment(self, client, logined_client, setup_data):
        endpoint = reverse("community:comment", kwargs={"comment_id": 2})

        # 로그인 사용자에 대한 테스트 - 자신의 댓글이 아님
        response = logined_client[1].delete(endpoint)

        assert response.status_code == 403

        # 로그인이 안 된 사용자에 대한 테스트
        response = client.delete(endpoint)

        assert response.status_code == 401

        # 로그인 사용자에 대한 테스트 - 자신의 댓글
        response = logined_client[0].delete(endpoint)

        assert response.status_code == 204
        assert response.data["message"] == "Comment deleted successfully"

        with pytest.raises(Comment.DoesNotExist):
            comment = Comment.objects.get(id=2)
