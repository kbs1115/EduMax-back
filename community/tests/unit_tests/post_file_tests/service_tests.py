from unittest.mock import patch
from rest_framework import exceptions
from rest_framework.exceptions import PermissionDenied
from community.serializers import FileSerializer
from community.service.post_service import PostService, PostsService
from community.tests.unit_tests.post_file_tests.conftests import *

from community.model.models import Post


class TestGetPostsService:

    def test_paging_with_invalid_page(
            self, mocked_function_get_posts_from_db_return_queryset, valid_post_instance_list
    ):
        invalid_page = len(valid_post_instance_list) + 1
        with pytest.raises(exceptions.NotFound):
            # page 제외 나머지 매개변수 안씀
            PostsService().get_posts(
                category=1,
                search_filter=1,
                kw=1,
                sort=1,
                page=invalid_page,
            )

    def test_paging_with_valid_page(
            self,
            mocked_function_get_posts_from_db_return_queryset,
            mocked_serializer_method_get_likes_count
    ):
        page = 1
        # page 제외 나머지 매개변수 안씀
        response = PostsService().get_posts(
            category=1,
            search_filter=1,
            kw=1,
            sort=1,
            page=page,
        )
        assert response

    def test_paging_with_valid_page_and_no_post(
            self,
            mocked_function_get_posts_from_db_return_empty_queryset,
            mocked_serializer_method_get_likes_count
    ):
        page = 1
        # page 제외 나머지 매개변수 안씀
        response = PostsService().get_posts(
            category=1,
            search_filter=1,
            kw=1,
            sort=1,
            page=page,
        )
        assert response


class TestPostServiceRetrieve:
    pass


class TestPostServiceCreate:
    def test_assert_called(
            self, mocker, mocked_create_files_method, common_user_instance
    ):
        mock_save = mocker.patch.object(PostCreateSerializer, "save")
        mock_is_valid = mocker.patch.object(PostCreateSerializer, "is_valid")
        mock_is_valid.return_value = True
        with patch("django.db.transaction.atomic"):
            PostService().create_post(
                category="EQ",
                title=123,
                content=123,
                html_content="<p>1</p>",
                author=common_user_instance,
            )
            mock_is_valid.assert_called_once()
            mock_save.assert_called_once()

    def test_post_create_permission_if_has_not_permission(self, common_user_instance):
        with pytest.raises(PermissionDenied):
            PostService().create_post(
                category="NO",
                title=123,
                content=123,
                html_content="<p>1</p>",
                author=common_user_instance,
            )

    def test_post_create_permission_if_has_permission(
            self, mocker, staff_user_instance
    ):
        mock_save = mocker.patch.object(PostCreateSerializer, "save")
        mock_is_valid = mocker.patch.object(PostCreateSerializer, "is_valid")
        mock_is_valid.return_value = True
        with patch("django.db.transaction.atomic"):
            PostService().create_post(
                category="NO",
                title=123,
                content=123,
                html_content="<p>1</p>",
                author=staff_user_instance,
            )
            mock_is_valid.assert_called_once()
            mock_save.assert_called_once()


class TestPostServiceDelete:
    def test_assert_called(
            self, mocker, mocked_get_post_obj, mocked_delete_files_method
    ):
        mock_delete = mocker.patch.object(Post, "delete")
        with patch("django.db.transaction.atomic"):
            PostService().delete_post(1)
            mocked_delete_files_method.assert_called_once()
            mock_delete.assert_called_once()


class TestPostServiceUpdate:
    def test_assert_called_if_files_state_is_replace(
            self, mocker, mocked_update_files_method, mocked_get_post_obj
    ):
        mock_save = mocker.patch.object(PostCreateSerializer, "save")
        mock_is_valid = mocker.patch.object(PostCreateSerializer, "is_valid")
        mock_is_valid.return_value = True

        with patch("django.db.transaction.atomic"):
            response = PostService().update_post(
                1,
                category="EQ",
                html_content="<p>1</p>",
                files="test_files",
                files_state=PostFilesState.REPLACE,
            )
            mock_is_valid.assert_called_once()
            mock_save.assert_called_once()
            mocked_update_files_method.assert_called_once()
            assert response

    def test_assert_called_if_files_state_is_replace_but_no_files(
            self, mocker, mocked_update_files_method, mocked_get_post_obj
    ):
        mock_save = mocker.patch.object(PostCreateSerializer, "save")
        mock_is_valid = mocker.patch.object(PostCreateSerializer, "is_valid")
        mock_is_valid.return_value = True

        with patch("django.db.transaction.atomic"):
            PostService().update_post(
                1,
                category="EQ",
                html_content="<p>1</p>",
                files_state=PostFilesState.REPLACE,
            )
            mock_is_valid.assert_called_once()
            mock_save.assert_called_once()
            mocked_update_files_method.assert_not_called()

    def test_assert_called_if_files_state_is_delete(
            self, mocker, mocked_delete_files_method, mocked_get_post_obj
    ):
        mock_save = mocker.patch.object(PostCreateSerializer, "save")
        mock_is_valid = mocker.patch.object(PostCreateSerializer, "is_valid")
        mock_is_valid.return_value = True

        with patch("django.db.transaction.atomic"):
            response = PostService().update_post(
                1,
                category="EQ",
                html_content="<p>1</p>",
                files_state=PostFilesState.DELETE,
            )
            mock_is_valid.assert_called_once()
            mock_save.assert_called_once()
            mocked_delete_files_method.assert_called_once()
            assert response


class TestFileService:
    def test_create_files_assert_called_successful(
            self, mocker, files_form_of_request_dot_files, mocked_s3_upload_file_method
    ):
        mock_is_valid = mocker.patch.object(FileSerializer, "is_valid")
        mock_is_valid.return_value = True
        mock_save = mocker.patch.object(FileSerializer, "save")

        files = files_form_of_request_dot_files.getlist("files")

        with patch("django.db.transaction.atomic"):
            FileService().create_files(files, Post)
            number_of_files = len(files)
            assert mock_is_valid.call_count == number_of_files
            assert mock_save.call_count == number_of_files
            assert mocked_s3_upload_file_method.call_count == number_of_files

    def test_delete_files_assert_called_successful(
            self,
            mocker,
            mocked_get_files_id_list,
            mocked_get_file_instance,
            mocked_s3_delete_file_method,
    ):
        mock_delete = mocker.patch.object(File, "delete")
        number_of_files = len(mocked_get_files_id_list.return_value)
        with patch("django.db.transaction.atomic"):
            FileService().delete_files(Post)
            assert mocked_get_file_instance.call_count == number_of_files
            assert mock_delete.call_count == number_of_files
            assert mocked_s3_delete_file_method.call_count == number_of_files
