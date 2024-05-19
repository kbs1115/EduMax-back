from rest_framework.exceptions import ValidationError, NotFound
import rest_framework.status as status
from django.db import transaction
from django.core.paginator import Paginator, EmptyPage
from rest_framework import status, exceptions

from community.serializers import CommentCreateSerializer, CommentRetrieveSerializer
from community.service.file_service import FileService
from community.model.access import (
    get_post_from_id,
    get_parent_post_id,
    get_comment_user_id,
    get_comment_from_id,
    get_comments_from_post,
    get_child_comments
)
from community.model.models import Comment
from community.domain.definition import PostFilesState, POST_LIST_PAGE_SIZE


class CommentService:
    # persistent layer의 get_comment_user_id를 불러온다.
    @classmethod
    def get_comment_user_id(cls, comment_id):
        return get_comment_user_id(comment_id)

    @classmethod
    def get_comment(cls, comment_id):
        try:
            comment = get_comment_from_id(comment_id)
            serializer = CommentRetrieveSerializer(comment)

            # view 함수로 넘겨주기
            return {
                "status": status.HTTP_200_OK,
                "message": "Comment retrieve successfully",
                "data": serializer.data,
            }
        # 해당 게시글이 존재하지않을 때
        # TODO: TRY구문 필요없습니다.
        except Comment.DoesNotExist:
            raise NotFound("Comment not found")

    @classmethod
    def get_comment_of_post_with_null_parent(cls, post_id):
        comments = get_comments_from_post(post_id)

        comment_array = []
        for comment in comments:
            if comment.parent_comment:
                continue

            serializer = CommentRetrieveSerializer(comment)
            comment_array.append(serializer.data)

        return {
            "status": status.HTTP_200_OK,
            "message": "Comment retrieve successfully",
            "data": comment_array,
        }

    @classmethod
    def get_child_comment(cls, comment_id):
        comments = get_child_comments(comment_id)

        comment_array = []
        for comment in comments:
            serializer = CommentRetrieveSerializer(comment)
            comment_array.append(serializer.data)

        return {
            "status": status.HTTP_200_OK,
            "message": "Comment retrieve successfully",
            "data": comment_array,
        }

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

    @classmethod
    def update_comment(cls, comment_id, content, html_content, files, files_state):
        serializer_data = {
            "content": content,
            "html_content": html_content,
        }

        comment = get_comment_from_id(comment_id)

        comment_update_serializer = CommentCreateSerializer(
            comment, data=serializer_data, partial=True
        )
        if not comment_update_serializer.is_valid():
            raise ValidationError(comment_update_serializer.errors)

        with transaction.atomic():
            comment = comment_update_serializer.save()

            # file 수정 또는 삭제
            if files_state:
                instance = FileService()
                if files_state == PostFilesState.REPLACE and files:
                    instance.put_files(files, comment)
                elif files_state == PostFilesState.DELETE:
                    instance.delete_files(comment)
                else:
                    return {
                        "message": "files_state is wrong",
                        "status_code": status.HTTP_400_BAD_REQUEST,
                    }
            return {
                "message": "Comment updated successfully",
                "status_code": status.HTTP_200_OK,
                "data": {
                    "id": comment.id,
                    "post_id": comment.post.id,
                    "author": comment.author.login_id,
                },
            }

    @classmethod
    def delete_comment(cls, comment_id):
        comment = get_comment_from_id(comment_id)

        with transaction.atomic():
            instance = FileService()
            instance.delete_files(comment)  # file 삭제
            comment.delete()  # comment 삭제
            return {
                "message": "Comment deleted successfully",
                "status_code": status.HTTP_204_NO_CONTENT,
            }
            
    def get_my_comments(self, user_nickname, page):
        comments = Comment.objects.filter(author__nickname=user_nickname)
        
        # paging 처리
        try:
            pagination = Paginator(comments, POST_LIST_PAGE_SIZE)
            page_obj = pagination.page(page).object_list
            list_size = len(page_obj)
        except EmptyPage:
            raise exceptions.NotFound

        # 직렬화
        comment_serializer = CommentRetrieveSerializer(page_obj, many=True)
        return {"status": status.HTTP_200_OK,
                "message": "comment list successfully",
                "data": {
                    "page": page,  # 현재 페이지
                    "page_size": POST_LIST_PAGE_SIZE,  # 한페이지당 게시글 개수
                    "total_page_count": comments.count() // POST_LIST_PAGE_SIZE + 1,
                    "list_size": list_size,  # 게시글 개수
                    "comment_list": comment_serializer.data,
            }
        }
