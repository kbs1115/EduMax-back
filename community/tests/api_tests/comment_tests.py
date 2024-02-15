import pytest
from django.urls import reverse

from community.model.models import File, Comment


class TestMakeCommentToPostAPI:

    @pytest.mark.django_db
    def test_create_comment(
        self, client, logined_client, setup_data, setup_files, mocked_s3_upload_file
    ):
        endpoint = reverse("community:post_comment", kwargs={"post_id": 2})

        # 로그인된 유저 테스트
        with open(setup_files[0].name, "rb") as image1, open(
            setup_files[1].name, "rb"
        ) as image2:
            response = logined_client[0].post(
                endpoint,
                {
                    "content": "testcontent3",
                    "html_content": "htmltestcontent3",
                    "files": [image1, image2],
                },
                format="multipart",
            )

        comment = Comment.objects.get(post_id=2)

        assert response.status_code == 201
        assert response.data["data"]["post_id"] == 2
        assert response.data["data"]["author"] == setup_data[4].login_id

        assert File.objects.filter(comment_id=comment.id)
        assert mocked_s3_upload_file.call_count == 2

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
    def test_create_comment(
        self,
        client,
        logined_client,
        setup_data,
        setup_files,
        mocked_s3_upload_file,
    ):
        endpoint = reverse("community:comment", kwargs={"comment_id": 1})

        # 로그인된 유저 테스트
        with open(setup_files[0].name, "rb") as image:
            response = logined_client[0].post(
                endpoint,
                {
                    "content": "testcontent3",
                    "html_content": "htmltestcontent3",
                    "files": image,
                },
                format="multipart",
            )

        comment = Comment.objects.get(parent_comment_id=1)

        assert response.status_code == 201
        assert response.data["data"]["post_id"] == setup_data[0].id
        assert response.data["data"]["author"] == setup_data[4].login_id

        mocked_s3_upload_file.assert_called_once()
        assert File.objects.get(comment_id=comment.id)

        # 로그인 안 된 유저 테스트
        response = client.post(
            endpoint,
            {"content": "testcontent3", "html_content": "htmltestcontent3"},
            format="json",
        )

        assert response.status_code == 401

    @pytest.mark.django_db
    def test_update_comment(
        self,
        client,
        logined_client,
        setup_data,
        setup_files,
        mocked_s3_upload_file,
        mocked_s3_delete_file,
        save_file_model,
    ):
        endpoint = reverse("community:comment", kwargs={"comment_id": 2})

        # 로그인된 유저 테스트(자신의 댓글)
        with open(setup_files[0].name, "rb") as image:
            response = logined_client[0].patch(
                endpoint,
                {
                    "content": "testcontent_updated",
                    "html_content": "htmltestcontent_updated",
                    "files_state": "REPLACE",
                    "files": image,
                },
                format="multipart",
            )

        file = File.objects.get(comment_id=2)

        assert file.file_location != "testlocation1"
        mocked_s3_upload_file.assert_called_once()
        mocked_s3_delete_file.assert_called_once()

        response = logined_client[0].patch(
            endpoint,
            {
                "content": "testcontent_updated2",
                "html_content": "htmltestcontent_updated",
                "files_state": "DELETE",
            },
            format="multipart",
        )

        assert response.status_code == 200
        assert response.data["data"]["post_id"] == setup_data[0].id
        assert response.data["data"]["author"] == setup_data[4].login_id
        assert Comment.objects.get(id=2).content == "testcontent_updated2"

        assert mocked_s3_delete_file.call_count == 2
        assert File.objects.all().count() == 0

        # 로그인된 유저 테스트(자신의 댓글) - File state wrong
        response = logined_client[0].patch(
            endpoint,
            {
                "content": "testcontent_updated",
                "html_content": "htmltestcontent_updated",
                "files_state": "eeee",
            },
            format="multipart",
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
            format="multipart",
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
            format="multipart",
        )

        assert response.status_code == 401

    @pytest.mark.django_db
    def test_delete_comment(
        self,
        client,
        logined_client,
        setup_data,
        mocked_s3_delete_file,
        save_file_model,
    ):
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

        mocked_s3_delete_file.assert_called_once()
        assert File.objects.all().count() == 0

        with pytest.raises(Comment.DoesNotExist):
            comment = Comment.objects.get(id=2)
