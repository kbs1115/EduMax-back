from django.http import JsonResponse
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView

from community.service.validation import login_required, restrict_post_create_permission, validate_query_params, \
    PostQueryParam, PostPathParam, validate_path_params
from community.service.post_service import PostService


class PostView(APIView):
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
            response = self.post_service.list_posts(validated_query_params)
            return JsonResponse(status=response.get("status_code"),
                                data={
                                    "message": response.get("message", None),
                                    "data": response.get("data", None)},
                                )

    # 고려해야할거: post 생성에서 permission 에 따라서
    # 공지사항을 쓸수있는지 없는지 다름. access 할수있어야함.
    # 로그인이 되지않는경우 access denied 한후 로그인 url을 던져준다.

    # validation 검사 필요함.
    # form이 넘어오잖슴. json 이 아니라 multy content type.
    @login_required
    @restrict_post_create_permission
    def post(self, request):
        request.parser_classes = [MultiPartParser]
        upload_files = request.data.FILES.get('files')
        category = request.data.get('category')
        title = request.data.get('title')
        content = request.data.get('content')
        author = request.user

        form = {'upload_files': upload_files,
                'title': title,
                'content': content,
                'author': author,
                'category': category
                }
        self.post_service.create_post(**form)

        # content type 이 json이 아니므로 파싱 필요함
        # 파싱이후 file은 aws에 저장하고 나머지는 db에 저장함.(service 단에서 처리)


class LikeView(APIView):
    def Post(self, request, post_id):
        pass
