from rest_framework import exceptions, status

from community.model.access import get_post_from_id, get_comment_from_id
from community.model.models import Post, Comment
from community.serializers import LikeCreateSerializer


class LikeService:
    @classmethod
    def get_serializer_data(cls, related_model_cls, pk, voter_id):
        if related_model_cls == "post":
            return {
                "post": pk,
                "user": voter_id
            }
        elif related_model_cls == "comment":
            return {
                "comment": pk,
                "user": voter_id
            }
        else:
            raise exceptions.ValidationError("post 혹은 comment만 추천할수있음")

    def generate_like(self, model_class, pk, voter_id):
        if model_class == "post":
            serializer_data = self.get_serializer_data(related_model_cls="post", pk=pk, voter_id=voter_id)

        elif model_class == "comment":
            serializer_data = self.get_serializer_data(related_model_cls="comment", pk=pk, voter_id=voter_id)
        else:
            raise exceptions.ValidationError("post 혹은 comment 만 추천할수있음")

        serializer = LikeCreateSerializer(data=serializer_data)

        if not serializer.is_valid():
            raise exceptions.ValidationError(str(serializer.errors))

        serializer.save()

        return {
            "message": "LIKE created successfully",
            "status_code": status.HTTP_201_CREATED
        }
