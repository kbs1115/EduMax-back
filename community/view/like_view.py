from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from community.model.access import get_post_from_id, get_comment_user_id
from community.model.like_access import check_like_inst_exist_with_post_id, check_like_inst_exist_with_comment_id
from community.model.models import Post, Comment
from community.model.post_access import get_post_user_id
from community.service.like_service import LikeService

# TODO: permission.py에 넣는건 어떠한가. 거기서 권한을 모두 관리하는것도 ㄱㅊ을듯
# class CannotLikeOwnPost(BasePermission):
#     def has_object_permission(self, request, view, post_id):
#         if request.user:
#             owner_id = get_post_user_id(post_id=post_id)
#             if owner_id == request.user.id:
#                 raise PermissionDenied()
#             return True
#         raise NotAuthenticated()

#
# class CannotLikeOwnComment(BasePermission):
#     def has_object_permission(self, request, view, comment_id):
#         if request.user:
#             owner_id = get_comment_user_id(comment_id=comment_id)
#             if owner_id == request.user.id:
#                 raise PermissionDenied()
#             return True
#         raise NotAuthenticated()
from edumax_account.models import User


class CanLikeOnce(BasePermission):
    def has_object_permission(self, request, view, inst_id):
        if request.user:
            if isinstance(view, LikeToPostView):
                if check_like_inst_exist_with_post_id(inst_id=inst_id, user=request.user):
                    raise PermissionDenied()
                return True
            elif isinstance(view, LikeToCommentView):
                if check_like_inst_exist_with_comment_id(inst_id=inst_id, user=request.user):
                    raise PermissionDenied()
                return True
        raise NotAuthenticated()


class LikeToPostView(APIView):
    permission_classes = [IsAuthenticated, CanLikeOnce]

    def post(self, request, post_id):
        self.check_object_permissions(request=request, obj=post_id)
        response = LikeService().generate_like(
            model_class="post",
            pk=post_id,
            voter_id=request.user.id
        )
        return Response(
            status=response.get("status_code"),
            data={
                "message": response.get("message", None),
                "data": response.get("data", None),
            }
        )


class LikeToCommentView(APIView):
    permission_classes = [IsAuthenticated, CanLikeOnce]

    def post(self, request, comment_id):
        self.check_object_permissions(request=request, obj=comment_id)
        response = LikeService().generate_like(
            model_class="comment",
            pk=comment_id,
            voter_id=request.user
        )
        return Response(
            status=response.get("status_code"),
            data={
                "message": response.get("message", None),
                "data": response.get("data", None),
            }
        )
