from rest_framework import exceptions, status

from community.model.access import get_post_from_id, get_comment_from_id
from community.model.models import Post, Comment
from community.serializers import LikeCreateSerializer


class LikeService:
    @classmethod
    def get_serializer_data(cls, related_model_inst, voter):
        if isinstance(Post, related_model_inst):
            return {
                "post": related_model_inst,
                "user": voter
            }
        elif isinstance(Comment, related_model_inst):
            return {
                "comment": related_model_inst,
                "user": voter
            }
        else:
            raise exceptions.ValidationError("post 혹은 comment만 추천할수있음")

    def generate_like(self, model_class, pk, voter):
        if isinstance(Post, model_class):
            inst = get_post_from_id(id=pk)

        elif isinstance(Post, model_class):
            inst = get_comment_from_id(comment_id=pk)

        else:
            raise exceptions.ValidationError("post 혹은 comment 만 추천할수있음")

        serializer_data = self.get_serializer_data(related_model_inst=inst, voter=voter)
        serializer = LikeCreateSerializer(data=serializer_data)

        if not serializer.is_valid():
            raise exceptions.ValidationError(str(serializer.errors))

        serializer.save()

        return {
            "message": "LIKE created successfully",
            "status_code": status.HTTP_201_CREATED
        }
