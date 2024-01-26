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
    POST_LIST_PAGE_SIZE, PostFilesState
from rest_framework import status

from community.service.file_service import FileService


class PostsService:
    parser_classes = [JSONParser]

    def get_posts(self, category, search_filter, kw, sort, page):
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

        # 직렬화
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


class PostService:
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def get_post(self, post_id):
        """
            <설명>
            - post_id를 받아서 select 후 알맞은 file model instances와 같이 return 한다.
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

    def create_post(self, category, title, content, html_content, files, author):
        """
            <설명>
                - post를 생성할때 쓰인다.
                - files 와 post에 필요한 form을 받아서 저장한다.
            <로직>
                1. service 단 validation ->필수필드 확인, category에 맞는 permision 확인
                2. post model 부분 분리 후 시리얼라이즈 유효성 검사
                3. 트랜잭션 단위 설정 후 post 저장
                4. file 부분 분리후 FileSerivce 인스턴스 생성
                5. file 부분 저장
        """

        # restrict_post_create_permission
        # if category == PostCategories.NOTICE:
        #     if not (author.is_superuser or author.is_staff):
        #         return {'message': 'Permission Denied',
        #                 "status_code": status.HTTP_403_FORBIDDEN}

        # request.data 로 부터 post model 분리
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

                # file 생성
                if files:
                    instance = FileService()
                    instance.create_files(files, post)
                return {"message": "Resource created successfully", "status_code": status.HTTP_201_CREATED}
        except ClientError as e:
            return {"message": str(e), "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR}
        except Exception as e:
            return {"message": str(e), "status_code": status.HTTP_400_BAD_REQUEST}

    def delete_post(self, post_id):
        """
            <설명>
                - post를 삭제할때 쓰인다.
                - post와 연관있는 파일들도 같이 삭제된다.
            <로직>
                1. service 단 validation -> post_id가 존재하는지 확인
                2. post 삭제전 s3의 file 리소스 위치 확인
                3. post_id 관련된 s3 files 삭제
                4. file model instances 삭제
                5. post model instance 삭제
        """
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
                instance.delete_files(post)  # file 삭제
                post.delete()  # post 삭제
                return {"message": "Resource deleted successfully", "status_code": status.HTTP_204_NO_CONTENT}
        except Exception as e:
            return {"message": str(e), "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR}

    def update_post(
            self,
            post_id,
            category,
            title,
            content,
            html_content,
            files_state,
            files,
            author
    ):
        """
            <설명>
                - post를 수정할때 쓰인다.
                - post와 연관있는 파일들도 같이 수정된다.
                - files_state 라는 keyword는 파일의 operation을 나타낸다.
                  -> value 종류: DELETE, REPLACE
                  -> service.define에 정의되어있음
            <로직>
                1. 인자로 받은 값을 토대로 변경될 필드를 확인
                   -> 변경되지않은 필드는 NONE이 들어가있음
                2. 변경해야하는 필드값를 시리얼라이즈
                3. 트랜잭션 단위 설정 후 post 부분 저장
                4. file부분 분리후 FileSerivce 인스턴스 생성
                5. file 부분 수정
        """
        post_data_for_serialize = dict()
        if category:
            post_data_for_serialize["category"] = category
        if title:
            post_data_for_serialize["title"] = title
        if content:
            post_data_for_serialize["content"] = content
        if html_content:
            post_data_for_serialize["html_content"] = html_content

        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "악악악악 post_id가 없는게 말이되냐",
            }
        # 직렬화
        post_serializer = PostCreateSerializer(post, data=post_data_for_serialize, partial=True)
        if not post_serializer.is_valid():
            return {"message": post_serializer.errors, "status_code": status.HTTP_400_BAD_REQUEST}
        try:
            with transaction.atomic():
                post = post_serializer.save()

                # file 수정 또는 삭제
                if files_state:
                    instance = FileService()
                    if files_state == PostFilesState.REPLACE and files:
                        instance.put_files(files, post)
                    elif files_state == PostFilesState.DELETE:
                        instance.delete_files(post)
                    else:
                        return {"message": "files_state is wrong", "status_code": status.HTTP_400_BAD_REQUEST}
                return {"message": "Resource updated successfully", "status_code": status.HTTP_200_OK}
        except ClientError as e:
            return {"message": str(e), "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR}
        except Exception as e:
            return {"message": str(e), "status_code": status.HTTP_400_BAD_REQUEST}
