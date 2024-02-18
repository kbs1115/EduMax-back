import pytest
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from community.view.like_view import LikeToPostView, LikeToCommentView


class TestLikeToPostView:

    def test_method_assert_called_with_valid_data(
            self,
            mocked_request,
            mocked_method_generate_like,
            mocked_function_check_like_inst_exist_with_post_id,
            user_instance
    ):
        response = LikeToPostView().post(mocked_request, post_id=1)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["message"] == "LIKE created successfully"

    def test_permission_if_like_twice(
            self,
            mocked_request,
            mocked_method_generate_like,
            mocked_function_check_like_inst_exist_with_post_id_if_exist,
            user_instance
    ):
        with pytest.raises(PermissionDenied):
            LikeToPostView().post(mocked_request, post_id=1)


class TestLikeToCommentView:
    def test_method_assert_called_with_valid_data(
            self,
            mocked_request,
            mocked_method_generate_like,
            mocked_function_check_like_inst_exist_with_comment_id,
            user_instance
    ):
        response = LikeToCommentView().post(mocked_request, comment_id=1)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["message"] == "LIKE created successfully"

    def test_permission_if_like_twice(
            self,
            mocked_request,
            mocked_method_generate_like,
            mocked_function_check_like_inst_exist_with_comment_id_if_exist,
            user_instance
    ):
        with pytest.raises(PermissionDenied):
            LikeToCommentView().post(mocked_request, comment_id=1)
