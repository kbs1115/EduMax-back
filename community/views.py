from django.http import JsonResponse
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.views import APIView

from community.service.validation import login_required, validate_query_params, \
    PostQueryParam, PostPathParam, validate_path_params
from community.service.post_service import PostService


class PostView(APIView):
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def __init__(self):
        self.post_service = PostService()

    # need validation query_param
    @validate_path_params(PostPathParam)
    @validate_query_params(PostQueryParam)
    def get(self, request, post_id=None, validated_query_params=None):
        # retrieve
        if post_id:
            post = self.post_service.retrieve_post(post_id)
            return JsonResponse(data=post)
        # list
        else:
            response = self.post_service.list_posts(request, validated_query_params)
            return JsonResponse(status=response.get("status_code"),
                                data={
                                    "message": response.get("message", None),
                                    "data": response.get("data", None)},
                                )

    # 고려해야할점: html_content 때문에 xss 방어가 작동할지 모르겠음
    @login_required
    def post(self, request):
        response = self.post_service.create_post(request)
        return JsonResponse(status=response.get("status_code"),
                            data={
                                "message": response.get("message", None),
                                "data": response.get("data", None)},
                            )

    # permission 설정 필요
    @validate_path_params(PostPathParam)
    @login_required
    def patch(self, request, post_id):
        response = self.post_service.update_post(request, post_id)
        return JsonResponse(status=response.get("status_code"),
                            data={
                                "message": response.get("message", None),
                                "data": response.get("data", None)},
                            )

    # permission 설정 필요
    @validate_path_params(PostPathParam)
    @login_required
    def delete(self, request, post_id):
        response = self.post_service.delete_post(post_id)
        return JsonResponse(status=response.get("status_code"),
                            data={
                                "message": response.get("message", None),
                                "data": response.get("data", None)},
                            )


class LikeView(APIView):
    def Post(self, request, post_id):
        pass
