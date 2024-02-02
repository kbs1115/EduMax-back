from rest_framework.exceptions import ValidationError, NotFound
import rest_framework.status as status
from django.db import transaction

from community.serializers import CommentCreateSerializer, CommentRetrieveSerializer
from community.service.file_service import FileService
from community.model.access import get_post_from_id, get_parent_post_id
from community.model.models import Comment


class CommentService:
    @classmethod
    def get_comment(cls, comment_id):
        try:
            comment = Comment.objects.get(pk=comment_id)
            serializer = CommentRetrieveSerializer(comment)

            # view 함수로 넘겨주기
            return {
                "status": status.HTTP_200_OK,
                "message": "Comment retrieve successfully",
                "data": serializer.data,
            }
        # 해당 게시글이 존재하지않을 때
        except Comment.DoesNotExist:
            raise NotFound("Comment not found")

    @classmethod
    def create_comment(
        cls, content, html_content, files, author, parent_comment_id, post_id
    ):
        """
        <설명>
            - comment를 생성할때 쓰인다.
            - files 와 comment에 필요한 form을 받아서 저장한다.
            - post_id가 None인 경우 parent_comment_id에서 post_id를 알아낸다.
        """
        if post_id is None:
            post_id = get_parent_post_id(parent_comment_id)

        post = get_post_from_id(post_id)
        serializer_data = {
            "content": content,
            "html_content": html_content,
            "author": author.id,
            "parent_comment": parent_comment_id,
            "post": post.id,
        }
        comment_serializer = CommentCreateSerializer(data=serializer_data)
        if not comment_serializer.is_valid():
            raise ValidationError(comment_serializer.errors)

        with transaction.atomic():
            comment = comment_serializer.save()

            # file 생성
            if files:
                instance = FileService()
                instance.create_files(files, comment)
            return {
                "message": "Comment created successfully",
                "status_code": status.HTTP_201_CREATED,
                "data": {
                    "id": comment.id,
                    "post_id": comment.post.id,
                    "author": comment.author.login_id,
                },
            }
