from rest_framework import status

from community.model.models import Post, Comment
from community.service.like_service import LikeService


class TestLikeService:
    def test_get_serializer_data_with_valid_data(
            self,
            user_instance,
            post_instance,
            comment_instance
    ):
        response = LikeService().get_serializer_data(related_model_inst=post_instance, voter=user_instance)
        assert response == {
            "post": post_instance,
            "user": user_instance
        }
        response = LikeService().get_serializer_data(related_model_inst=comment_instance, voter=user_instance)
        assert response == {
            "comment": comment_instance,
            "user": user_instance
        }

    def test_generate_like_method_assert_called_with_valid_data(
            self,
            mocker,
            mocked_serializer_save,
            mocked_is_valid,
            user_instance,
            post_instance,
            comment_instance
    ):
        mocker.patch(
            "community.service.like_service.get_post_from_id",
            return_value=post_instance
        )
        mocker.patch(
            "community.service.like_service.get_comment_from_id",
            return_value=comment_instance
        )

        response = LikeService().generate_like(model_class="post", pk=1, voter=user_instance)
        mocked_is_valid.assert_called()
        mocked_serializer_save.assert_called()
        assert response["message"] == "LIKE created successfully"
        assert response["status_code"] == status.HTTP_201_CREATED

        response = LikeService().generate_like(model_class="comment", pk=1, voter=user_instance)
        mocked_is_valid.assert_called()
        mocked_serializer_save.assert_called()
        assert response["message"] == "LIKE created successfully"
        assert response["status_code"] == status.HTTP_201_CREATED
