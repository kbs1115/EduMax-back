from django.http import JsonResponse
from rest_framework.views import APIView
from service.post_service import PostService


class PostView(APIView):
    def __init__(self):
        self.post_service = PostService()

    # 관심사 분리
    def get(self, request):
        query_params = request.GET
        title = query_params.get("title")
        posts = self.post_service.get_posts(title)  # json 형식으로 return
        return JsonResponse(data=posts)
