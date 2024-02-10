# post test 해야할거:
# 1. 제대로 찾아오는지-> 관련된 파일이 있다면 해당파일도
# 잘 긁어오는지 확인해야함.
# 2. 잘 생성하는지, file 넣어줬을때 잘 생성하는지 테스트
# 3. auth 잘 막는지
# 4. 잘 수정하는지
# 5. 잘 삭제하는지
from django.urls import reverse

from community.tests.api_tests.conftests import *


class TestPostViewAPi:
    @pytest.mark.django_db
    def test_create_post(
            self, client, logined_client, setup_files, mocked_s3_upload_file
    ):
        assert 0 == Post.objects.all().count()
        assert 0 == File.objects.all().count()
        endpoint = reverse("community:post")

        # 로그인된 유저 테스트
        with open(setup_files[0].name, "rb") as image1, open(
                setup_files[1].name, "rb"
        ) as image2:
            response = logined_client[0].post(
                endpoint,
                {
                    "title": "test_title",
                    "content": "test_content",
                    "html_content": "test_html_content",
                    "category": "KQ",
                    "files": [image1, image2]
                },
                format="multipart",
            )
        assert 1 == Post.objects.all().count()
        assert response.status_code == 201

        assert 2 == File.objects.all().count()
        assert mocked_s3_upload_file.call_count == 2

        # 로그인 안 된 유저 테스트
        response = client.post(
            endpoint,
            {"title": "test_title",
             "content": "test_content",
             "html_content": "test_html_content",
             "category": "KQ", },
            format="json",
        )

        assert response.status_code == 401

    @pytest.mark.django_db
    def test_retrieve_comment(self, client, logined_client, setup_data):
        endpoint = reverse("community:post", kwargs={"post_id": 1})

        # 로그인 사용자에 대한 테스트
        response = logined_client[0].get(endpoint)
        data = response.json()
        print(data)
        assert response.status_code == 200

        assert data.get("message") == "post retrieve successfully"
        assert data.get("data").get("title") == setup_data[0].title
        assert data.get("data").get("html_content") == setup_data[0].html_content
        assert data.get("data").get("author") == setup_data[0].author.nickname

        # 비로그인 사용자에 대한 테스트
        response = client.get(endpoint)

        data = response.json()

        assert response.status_code == 200

        assert data.get("message") == "post retrieve successfully"
        assert data.get("data").get("title") == setup_data[0].title
        assert data.get("data").get("html_content") == setup_data[0].html_content
        assert data.get("data").get("author") == setup_data[0].author.nickname

    @pytest.mark.django_db
    def test_update_post(
            self,
            client,
            logined_client,
            setup_data,
            setup_files,
            mocked_s3_upload_file,
            mocked_s3_delete_file,
            save_file_model_fk_post,
    ):
        endpoint = reverse("community:post", kwargs={"post_id": 1})

        # 로그인된 유저 테스트(자신의 게시글)
        with open(setup_files[0].name, "rb") as image:
            response = logined_client[0].patch(
                endpoint,
                {
                    "title": "test_title",
                    "content": "test_content",
                    "html_content": "test_html_content",
                    "category": "KQ",
                    "files_state": "REPLACE",
                    "files": image,
                },
                format="multipart",
            )

            file = File.objects.get(post_id=1)
            assert response.status_code == 200
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
            data = response.json()

            assert response.status_code == 200
            assert data.get("message") == "Resource updated successfully"
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
    def test_delete_post(
            self,
            client,
            logined_client,
            setup_data,
            mocked_s3_delete_file,
            save_file_model_fk_post,
    ):
        endpoint = reverse("community:post", kwargs={"post_id": 1})

        # 로그인 사용자에 대한 테스트 - 자신의 댓글이 아님
        response = logined_client[1].delete(endpoint)

        assert response.status_code == 403

        # 로그인이 안 된 사용자에 대한 테스트
        response = client.delete(endpoint)

        assert response.status_code == 401

        # 로그인 사용자에 대한 테스트 - 자신의 댓글
        response = logined_client[0].delete(endpoint)

        assert response.status_code == 204

        mocked_s3_delete_file.assert_called_once()
        assert File.objects.all().count() == 0

        with pytest.raises(Post.DoesNotExist):
            Post.objects.get(id=1)
