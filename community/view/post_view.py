from django.http import JsonResponse
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated
from rest_framework.views import APIView

from account.models import User
from community.service.validation import validate_query_params, \
    PostQueryParam, PostPathParam, validate_path_params, validate_body_request, CreatePostRequestBody, \
    UpdatePostRequestBody
from community.service.post_service import PostService, PostsService


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj_id):
        if request.user:
            if obj_id == request.user.id:
                return True
            raise PermissionDenied()
        raise NotAuthenticated()


class GetPostsView(APIView):
    parser_classes = [JSONParser]

    def __init__(self):
        self.post_service = PostsService()

    @validate_query_params(PostQueryParam)
    def get(self, request, validated_query_params):
        params = {
            "page": validated_query_params.page,
            "category": validated_query_params.category,
            "search_filter": validated_query_params.search_filter,
            "kw": validated_query_params.q,
            "sort": validated_query_params.sort
        }
        response = self.post_service.get_posts(**params)

        return JsonResponse(status=response.get("status_code"),
                            data={
                                "message": response.get("message", None),
                                "data": response.get("data", None)},
                            )


class PostView(APIView):
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    permission_classes = [IsAuthenticated | ReadOnly, IsOwner]

    def __init__(self):
        self.post_service = PostService()

    @validate_path_params(PostPathParam)
    def get(self, request, post_id):
        # retrieve
        response = self.post_service.get_post(post_id)
        return JsonResponse(status=response.get("status_code"),
                            data={
                                "message": response.get("message", None),
                                "data": response.get("data", None)},
                            )

    @validate_body_request(CreatePostRequestBody)
    def post(self, request, validated_request_body):
        body = {
            "category": validated_request_body.category,
            "content": validated_request_body.content,
            "html_content": validated_request_body.html_content,
            "title": validated_request_body.title,
            'files': request.FILES.getlist('files', None),
            "author": request.user
        }
        response = self.post_service.create_post(**body)
        return JsonResponse(status=response.get("status_code"),
                            data={
                                "message": response.get("message", None),
                                "data": response.get("data", None)},
                            )

    @validate_body_request(UpdatePostRequestBody)
    @validate_path_params(PostPathParam)
    def patch(self, request, post_id, validated_request_body):
        # instance permission 확인
        obj_id = PostService.get_post_user_id(post_id)
        self.check_object_permissions(request, obj_id)

        body = {
            "category": validated_request_body.category,
            "content": validated_request_body.content,
            "html_content": validated_request_body.html_content,
            "title": validated_request_body.title,
            'files_state': validated_request_body.files_state,
            'files': request.FILES.getlist('files', None),
            "author": request.user
        }
        response = self.post_service.update_post(post_id, **body)
        return JsonResponse(status=response.get("status_code"),
                            data={
                                "message": response.get("message", None),
                                "data": response.get("data", None)},
                            )

    @validate_path_params(PostPathParam)
    def delete(self, request, post_id):
        # instance permission 확인
        obj_id = PostService.get_post_user_id(post_id)
        self.check_object_permissions(request, obj_id)

        response = self.post_service.delete_post(post_id)
        return JsonResponse(status=response.get("status_code"),
                            data={
                                "message": response.get("message", None),
                                "data": response.get("data", None)},
                            )


class LikeView(APIView):
    def Post(self, request, post_id):
        pass
