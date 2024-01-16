import uuid

import status as status
from botocore.exceptions import ClientError
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q, Count
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser

from community.models import Post
from community.serializers import PostSerializer, FileSerializer
from community.service.define import PostSearchFilterParam, PostSortCategoryParam
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

from community.service.validation import restrict_post_create_permission


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
                default_storage.save(path, ContentFile(file.read()))
            except ClientError as e:
                raise e
            except Exception as e:
                raise e

    @classmethod
    def make_files_path(cls, files):
        files_path = []
        unique_id = str(uuid.uuid4())
        for file in files:
            file_path = f"{unique_id}_{file.name}"
            files_path.append(file_path)
        return files_path


class PostService:
    """
        <설명>
        - post_id를 받아서 select 후 return 한다.
        - 만약 post_id 가 없을 시 DoesNotExist을 발생시킨다.
    """
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def retrieve_post(self, post_id):
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

    def list_posts(self, validated_query_params):
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
        page = validated_query_params.page
        sort = validated_query_params.sort

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
            if posts and sort == PostSortCategoryParam.CREATE_AT:
                posts = posts.order("-" + str(PostSortCategoryParam.CREATE_AT))
            elif posts and sort == PostSortCategoryParam.MOST_LIKE:
                posts = posts.annotate(like_count=Count('likes')).order_by('-like_count')

        except Exception as e:
            return {"status_code": status.HTTP_500_INTERNAL_SERVER_ERROR, "message": str(e)}

        # paging 처리
        try:
            paginator = Paginator(posts, 15)
            page_obj = paginator.get_page(page)
        except Exception as e:
            return {"status_code": status.HTTP_500_INTERNAL_SERVER_ERROR, "message": str(e)}

        # 시리얼라이즈
        try:
            if page_obj:
                serializer = PostSerializer(page_obj)
                response = {"status_code": status.HTTP_200_OK,
                            "message": "posts listed successfully",
                            "data": serializer.data,
                            }
            else:
                # 만약 없으면 빈배열
                response = {"status_code": status.HTTP_200_OK,
                            "message": "there are no posts at all",
                            "data": {},
                            }
        except Exception as e:
            return {"status_code": status.HTTP_500_INTERNAL_SERVER_ERROR, "message": str(e)}
        return response

    # category validation 필요함. category, content, title 이 필수적으로 필요하다.
    # post가 file이랑 같이 원자단위로 트랜잭션이 발생해야함.
    # 그러려면 이게 file을 먼저 올리고 그다음 하는게 맞아보이는데요.
    @restrict_post_create_permission
    def create_post(self, request):
        try:
            category = request.data['category']
            content = request.data['content']
            title = request.data['title']
            author = request.user
        except KeyError as e:
            return {"status_code": status.HTTP_204_NO_CONTENT, "message": f"필수 필드 누락: {e}"}

        post_data = {'category': category,
                     'content': content,
                     'title': title,
                     'author': author
                     }
        post_serializer = PostSerializer(data=post_data)
        if not post_serializer.is_valid():
            return {"message": post_serializer.errors, "status_code": status.HTTP_400_BAD_REQUEST}

        files = request.FILES.getlist('files', None)
        files_path = UploadService.make_files_path(files)
        serializers = []

        for f_path in files_path:
            file_data = {"file_url": f_path, "post": post_data}
            file_serializer = FileSerializer(data=file_data)

            if file_serializer.is_valid():
                serializers.append(file_serializer)
            else:
                return {"message": file_serializer.errors, "status_code": status.HTTP_400_BAD_REQUEST}

        try:
            with transaction.atomic():
                post_serializer.save()
                for file_ser in serializers:
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
