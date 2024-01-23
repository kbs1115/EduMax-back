import status as status
from botocore.exceptions import ClientError
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q, Count
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser

from account.models import User
from community.domain.categories import PostCategories
from community.models import Post
from community.serializers import PostRetrieveSerializer, PostListSerializer, PostCreateSerializer
from community.service.define import PostSearchFilterParam, PostSortCategoryParam, \
    POST_LIST_PAGE_SIZE
from rest_framework import status

from community.service.file_service import FileService


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
            serializer = PostRetrieveSerializer(post)
            # view 함수로 넘겨주기
            return {"status": status.HTTP_200_OK,
                    "message": "post retrieve successfully",
                    "data": serializer.data,
                    }
        # 해당 게시글이 존재하지않을 때
        except Post.DoesNotExist:
            return {
                "status": status.HTTP_404_NOT_FOUND,
                "message": f"post id = {post_id} does not exist",
            }
        # 그외의 에러
        except Exception as e:
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
            pagination = Paginator(posts, POST_LIST_PAGE_SIZE)
            page_obj = pagination.page(page).object_list
            list_size = len(page_obj)
        except Exception as e:
            return {"status_code": status.HTTP_500_INTERNAL_SERVER_ERROR, "message": str(e)}
        try:
            post_serializer = PostListSerializer(page_obj, many=True)
            return {"status": status.HTTP_200_OK,
                    "message": "post list successfully}",
                    "data": {"page": page,  # 현재 페이지
                             "page_size": POST_LIST_PAGE_SIZE,  # 한페이지당 게시글 개수
                             "list_size": list_size,  # 게시글 개수
                             "post_list": post_serializer.data},
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
            return {"status_code": status.HTTP_400_BAD_REQUEST, "message": f"필수 필드 누락: {e}"}

        # request.data 로 부터 post model부분 분리
        post_data = {'category': category,
                     'html_content': html_content,
                     'content': content,
                     'title': title,
                     'author': author.id
                     }
        post_serializer = PostCreateSerializer(data=post_data)
        if not post_serializer.is_valid():
            return {"message": post_serializer.errors, "status_code": status.HTTP_400_BAD_REQUEST}
        try:
            with transaction.atomic():
                post = post_serializer.save()

                # file 처리
                files = request.FILES.getlist('files', None)
                if files:
                    instance = FileService()
                    instance.create_files(request, post)
                return {"message": "Resource created successfully", "status_code": status.HTTP_201_CREATED}
        except ClientError as e:
            return {"message": str(e), "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR}
        except Exception as e:
            return {"message": str(e), "status_code": status.HTTP_400_BAD_REQUEST}

    def delete_post(self, post_id):
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return {
                "status": status.HTTP_404_NOT_FOUND,
                "message": f"post id = {post_id} does not exist or already delete",
            }
        try:
            with transaction.atomic():
                instance = FileService()
                instance.delete_files(post)
                post.delete()
                return {"message": "Resource deleted successfully", "status_code": status.HTTP_204_NO_CONTENT}
        except Exception as e:
            return {"message": str(e), "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR}

    def update_post(self, request, post_id):
        try:
            post_data_for_serialize = dict()
            post_field_mapping = {
                'title': 'title',
                'content': 'content',
                'html_content': 'html_content',
                'category': 'category',
            }
            for field in post_field_mapping.keys():
                if request.data.get(field, None):
                    post_data_for_serialize[field] = request.data[field]

        except Exception as e:
            return {"message": str(e), "status_code": status.HTTP_400_BAD_REQUEST}
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "악악악악 post_id가 없는게 말이되냐",
            }
        post_serializer = PostCreateSerializer(post, data=post_data_for_serialize, partial=True)
        if not post_serializer.is_valid():
            return {"message": post_serializer.errors, "status_code": status.HTTP_400_BAD_REQUEST}
        try:
            with transaction.atomic():
                post = post_serializer.save()
                files_state = request.data.get('files_state', None)
                if files_state:
                    instance = FileService()
                    instance.put_files(request, post)
                return {"message": "Resource updated successfully", "status_code": status.HTTP_200_OK}
        except ClientError as e:
            return {"message": str(e), "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR}
        except Exception as e:
            return {"message": str(e), "status_code": status.HTTP_400_BAD_REQUEST}
