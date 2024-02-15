from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.response import Response

from .post_view import IsOwner, ReadOnly
from community.view.validation import (
    validate_body_request,
    validate_path_params,
    CreateCommentRequestBody,
    UpdateCommentRequestBody,
    PostPathParam,
    CommentPathParam,
)
from community.service.comment_service import CommentService


class MakeCommentToPostView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    @validate_body_request(CreateCommentRequestBody)
    @validate_path_params(PostPathParam)
    def post(self, request, post_id, validated_request_body):
        body = {
            "content": validated_request_body.content,
            "html_content": validated_request_body.html_content,
            "files": request.FILES.getlist("files", None),
            "author": request.user,
            "parent_comment_id": None,
            "post_id": post_id,
        }
        response = CommentService.create_comment(**body)
        return Response(
            status=response.get("status_code"),
            data={
                "message": response.get("message", None),
                "data": response.get("data", None),
            },
        )


class CommentView(APIView):
    permission_classes = [IsAuthenticated | ReadOnly, IsOwner]
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    # id에 해당하는 comment를 조회한다.
    @validate_path_params(CommentPathParam)
    def get(self, request, comment_id):
        res = CommentService.get_comment(comment_id)
        return Response(
            status=res.get("status"),
            data={
                "message": res.get("message", None),
                "data": res.get("data", None),
            },
        )

    # id에 해당하는 comment에 comment를 단다.
    @validate_body_request(CreateCommentRequestBody)
    @validate_path_params(CommentPathParam)
    def post(self, request, comment_id, validated_request_body):
        body = {
            "content": validated_request_body.content,
            "html_content": validated_request_body.html_content,
            "files": request.FILES.getlist("files", None),
            "author": request.user,
            "parent_comment_id": comment_id,
            "post_id": None,
        }
        response = CommentService.create_comment(**body)
        return Response(
            status=response.get("status_code"),
            data={
                "message": response.get("message", None),
                "data": response.get("data", None),
            },
        )

    @validate_body_request(UpdateCommentRequestBody)
    @validate_path_params(CommentPathParam)
    def patch(self, request, comment_id, validated_request_body):
        obj_id = CommentService.get_comment_user_id(comment_id)
        self.check_object_permissions(request, obj_id)

        body = {
            "content": validated_request_body.content,
            "html_content": validated_request_body.html_content,
            "files": request.FILES.getlist("files", None),
            "files_state": validated_request_body.files_state,
        }

        response = CommentService.update_comment(comment_id, **body)
        return Response(
            status=response.get("status_code"),
            data={
                "message": response.get("message", None),
                "data": response.get("data", None),
            },
        )

    @validate_path_params(CommentPathParam)
    def delete(self, request, comment_id):
        obj_id = CommentService.get_comment_user_id(comment_id)
        self.check_object_permissions(request, obj_id)

        response = CommentService.delete_comment(comment_id)
        return Response(
            status=response.get("status_code"),
            data={
                "message": response.get("message", None),
            },
        )
