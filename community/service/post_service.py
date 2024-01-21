import uuid
from django.forms.models import model_to_dict
import status as status
from botocore.exceptions import ClientError
from django.contrib.auth.hashers import make_password
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q, Count
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser

from account.models import User
from community.domain.categories import PostCategories
from community.models import Post, File
from community.serializers import PostSerializer, FileSerializer, PostListSerializer
from community.service.define import PostSearchFilterParam, PostSortCategoryParam, PostPageNumberPagination
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist




class UploadService:
    # file을 올리기전에 여러 validation이 필요할것으로 예상되지만 일단 pass
    @classmethod
    def upload_files(cls, files, paths):
        if not len(files) == len(paths):
            raise ValueError("The number of files and paths must be equal.")
        for i in range(len(files)):
            file = files[i]
            path = paths[i]
            try:
                default_storage.save(path, ContentFile(file.read()))  # 장고에서 모든 request.Files는 contentFile instance에 속함
            except ClientError as e:
                raise e
            except Exception as e:
                raise e

    @classmethod
    def download_files(cls, paths):
        # front 에서 file path 만 주고 직접 다운로드 할수 있게 한다.
        pass

    @classmethod
    def make_files_path(cls, files):
        # s3 에서 해당 파일의 id 역할을 한다.
        files_path = []
        for file in files:
            unique_id = str(uuid.uuid4())
            file_path = f"media/{unique_id}_{file.name}"
            files_path.append(file_path)
        return files_path


class PostService:
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def retrieve_post(self, post_id):
        """
            <설명>
            - post_id를 받아서 select 후 return 한다.
            - 만약 post_id 가 없을 시 DoesNotExist을 발생시킨다.
        """
        try:
            post = Post.objects.get(pk=post_id)
            serializer = PostSerializer(post)
            # view 함수로 넘겨주기
            return {"status": status.HTTP_200_OK,
                    "message": "post retrieve successfully",
                    "data": serializer.data,
                    }

        # 해당 게시글이 존재하지않을 때
        except Post.DoesNotExist:
            # view 함수로 넘겨주기
            return {
                "status": status.HTTP_404_NOT_FOUND,
                "message": f"post id = {post_id} does not exist",
            }
        # 그외의 에러
        except Exception as e:
            # view 함수로 넘겨주기
            return {"status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": str(e)}

    def list_posts(self, request, validated_query_params):
        """
            <설명>
                - validator을 지난 param을 가지고 조건에 맞게 select후 return.
                - param에 대한 정의 -> community.service.define
            <로직>
                1. category에 맞는 게시글들 select
                2. search_filter 에 맞는 kw select (kw 가 없을시 전체 posts)
                3. sort_category 에 맞는 순서로 게시글 정렬
                4. 15개 기준으로 페이징 처리
                5. 직렬화 후 return

        """
        # validation 이후의 쿼리 파라매터
        category = validated_query_params.category
        search_filter = validated_query_params.search_filter
        kw = validated_query_params.q
        sort = validated_query_params.sort
        page = validated_query_params.page
        try:
            # category에 따른 정렬
            posts = Post.objects.filter(category=category).all()

            # kw에 따른 정렬
            if kw and search_filter == PostSearchFilterParam.TOTAL:
                posts = posts.filter(
                    Q(author__nickname__icontains=kw) | Q(content__icontains=kw) | Q(title__icontains=kw)).distinct()
            elif kw and search_filter == PostSearchFilterParam.AUTHOR:
                posts = posts.filter(Q(author__nickname__icontains=kw))
            elif kw and search_filter == PostSearchFilterParam.CONTENT:
                posts = posts.filter(Q(content__icontains=kw))
            elif kw and search_filter == PostSearchFilterParam.TITLE:
                posts = posts.filter(Q(title__icontains=kw))

            # posts가 빈 쿼리셋이 아닐시 sort에 맞게 정렬
            if posts and sort == PostSortCategoryParam.CREATED_AT:
                posts = posts.order_by("-" + str(PostSortCategoryParam.CREATED_AT))
            elif posts and sort == PostSortCategoryParam.MOST_LIKE:
                posts = posts.annotate(like_count=Count('likes')).order_by('-like_count')

        except Exception as e:
            return {"status_code": status.HTTP_500_INTERNAL_SERVER_ERROR, "message": str(e)}

        # paging 처리
        try:
            pagination = Paginator(posts, 15)
            page_obj = pagination.page(page).object_list
        except Exception as e:
            return {"status_code": status.HTTP_500_INTERNAL_SERVER_ERROR, "message": str(e)}
        try:
            post_serializer = PostListSerializer(page_obj, many=True)
            return {"status": status.HTTP_200_OK,
                    "message": f"page: {page} list successfully",
                    "data": post_serializer.data,
                    }
        except Exception as e:
            return {"status_code": status.HTTP_500_INTERNAL_SERVER_ERROR, "message": str(e)}

    def create_post(self, request):
        # service layer validation
        try:
            category = request.data['category']
            content = request.data['content']
            title = request.data['title']
            html_content = request.data['html_content']

            # user 가 없어서 임의로 만든다음 집어넣었음
            author = User.objects.get(id=1)
            # 만약 user 부분이 merge 되면 윗줄 삭제, 밑의 주석 해체
            # author = request.user

            # restrict_post_create_permission
            if category == PostCategories.NOTICE:
                if not (author.is_superuser or author.is_staff):
                    return {'message': 'Permission Denied',
                            "status_code": status.HTTP_403_FORBIDDEN}
        except KeyError as e:
            return {"status_code": status.HTTP_204_NO_CONTENT, "message": f"필수 필드 누락: {e}"}

        # request.data 로 부터 post model 부분 분리
        post_data = {'category': category,
                     'html_content': html_content,
                     'content': content,
                     'title': title,
                     'author': author.id
                     }
        post_serializer = PostSerializer(data=post_data)
        if not post_serializer.is_valid():
            return {"message": post_serializer.errors, "status_code": status.HTTP_400_BAD_REQUEST}

        # file 가져오고 file_path 생성
        files = request.FILES.getlist('files', None)
        files_path = UploadService.make_files_path(files)
        try:
            with transaction.atomic():
                post = post_serializer.save()

                if files:
                    serialized_list = []
                    for f_path in files_path:
                        file_data = {"file_location": f_path, "post": post.id}
                        file_serializer = FileSerializer(data=file_data)

                        if file_serializer.is_valid():
                            serialized_list.append(file_serializer)
                        else:
                            transaction.set_rollback(True)
                            return {"message": file_serializer.errors, "status_code": status.HTTP_400_BAD_REQUEST}
                    for file_ser in serialized_list:
                        file_ser.save()
                    UploadService.upload_files(files, files_path)

                return {"message": "create post object successfully", "status_code": status.HTTP_201_CREATED}
        except ClientError as e:
            return {"message": str(e), "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR}
        except Exception as e:
            return {"message": str(e), "status_code": status.HTTP_400_BAD_REQUEST}

    def delete_post(self, request, post_id):
        pass

    def update_post(self, request, post_id):
        # 프론트에서 해당 게시글을 알아서 수정한다음 수정본을 서버로 던져주는 개념
        pass
