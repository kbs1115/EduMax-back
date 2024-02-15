import pytest
from rest_framework import status
from community.view.comment_view import MakeCommentToPostView, CommentView


class TestMakeCommentToPostView:
    view = MakeCommentToPostView()

    def test_post(
        self,
        validated_create_comment_request_body,
        mocked_create_comment,
        mocked_post_request,
    ):
        mocked_create_comment.return_value = {
            "message": "Comment created successfully",
            "status_code": status.HTTP_201_CREATED,
            "data": {
                "id": 2,
                "post_id": 3,
                "author": "testuser",
            },
        }

        response = MakeCommentToPostView.post.__wrapped__.__wrapped__(
            self.view, mocked_post_request, 3, validated_create_comment_request_body
        )

        assert response.status_code == 201
        assert response.data == {
            "message": "Comment created successfully",
            "data": {
                "id": 2,
                "post_id": 3,
                "author": "testuser",
            },
        }


class TestMakeCommentToPostView:
    view = CommentView()

    def test_get(self, mocked_get_comment, mocked_get_request):
        mocked_get_comment.return_value = {
            "status": 200,
            "message": "Comment retrieve successfully",
            "data": "mocked_comment_data",
        }

        response = CommentView.get.__wrapped__(
            self.view, mocked_get_request, mocked_get_comment
        )

        assert response.status_code == 200
        assert response.data == {
            "message": "Comment retrieve successfully",
            "data": "mocked_comment_data",
        }

    def test_post(
        self,
        validated_create_comment_request_body,
        mocked_create_comment,
        mocked_post_request,
    ):
        mocked_create_comment.return_value = {
            "message": "Comment created successfully",
            "status_code": status.HTTP_201_CREATED,
            "data": "mocked_comment_data",
        }

        response = CommentView.post.__wrapped__.__wrapped__(
            self.view, mocked_post_request, 3, validated_create_comment_request_body
        )

        mocked_create_comment.assert_called_once()
        assert response.status_code == 201
        assert response.data == {
            "message": "Comment created successfully",
            "data": "mocked_comment_data",
        }

    def test_patch(
        self,
        validated_update_comment_request_body,
        mocked_update_comment,
        mocked_check_object_permissions,
        mocked_post_request,
        mocked_get_comment_user_id,
    ):
        mocked_update_comment.return_value = {
            "message": "Comment updated successfully",
            "status_code": status.HTTP_200_OK,
            "data": "mocked_comment_data",
        }

        response = CommentView.patch.__wrapped__.__wrapped__(
            self.view, mocked_post_request, 3, validated_update_comment_request_body
        )

        mocked_get_comment_user_id.assert_called_once()
        mocked_check_object_permissions.assert_called_once()
        mocked_update_comment.assert_called_once()

        assert response.status_code == 200
        assert response.data == {
            "message": "Comment updated successfully",
            "data": "mocked_comment_data",
        }

    def test_delete(
        self,
        mocked_delete_comment,
        mocked_check_object_permissions,
        mocked_get_comment_user_id,
        mocked_get_request,
    ):
        mocked_delete_comment.return_value = {
            "message": "Comment deleted successfully",
            "status_code": status.HTTP_204_NO_CONTENT,
        }

        response = CommentView.delete.__wrapped__(self.view, mocked_get_request, 3)

        mocked_get_comment_user_id.assert_called_once()
        mocked_check_object_permissions.assert_called_once()
        mocked_delete_comment.assert_called_once()

        assert response.status_code == 204
        assert response.data == {
            "message": "Comment deleted successfully",
        }
