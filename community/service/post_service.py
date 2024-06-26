import status as status
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator, EmptyPage
from django.db import transaction
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from django.core.cache import cache

from community.model.post_access import get_posts_from_db, get_post_instance
from community.model.models import Like
from community.serializers import PostRetrieveSerializer, PostListSerializer, PostCreateSerializer
from community.domain.definition import POST_LIST_PAGE_SIZE, PostFilesState
from rest_framework import status, exceptions

from community.service.file_service import FileService
from community.service.permission import only_staff_can_create_post_notice


class PostsService:
    parser_classes = [JSONParser]

    def get_posts(
            self,
            category,
            search_filter,
            kw,
            sort,
            page,
            my_name=None
    ):
        """
            <설명>
                - validator을 통과한 query_param을 가지고 조건에 맞게 select후 return.
                - param에 대한 정의 -> community.service.define
            <로직>
                1. category에 맞는 게시글들 select
                2. search_filter 에 맞는 kw select (kw 가 없을시 전체 posts)
                3. sort_category 에 맞는 순서로 게시글 정렬
                4. 15개 기준으로 페이징 처리
                5. 직렬화 후 return

        """
        # 조건에 맞는 posts select
        posts = get_posts_from_db(category, search_filter, kw, sort, my_name)

        # paging 처리
        try:
            pagination = Paginator(posts, POST_LIST_PAGE_SIZE)
            page_obj = pagination.page(page).object_list
            list_size = len(page_obj)
        except EmptyPage:
            raise exceptions.NotFound

        # 직렬화
        post_serializer = PostListSerializer(page_obj, many=True)
        return {"status": status.HTTP_200_OK,
                "message": "post list successfully",
                "data": {"page": page,  # 현재 페이지
                         "page_size": POST_LIST_PAGE_SIZE,  # 한페이지당 게시글 개수
                         "total_page_count": (posts.count() + POST_LIST_PAGE_SIZE - 1) // POST_LIST_PAGE_SIZE,
                         "list_size": list_size,  # 게시글 개수
                         "post_list": post_serializer.data,
                         }}

    def get_like_posts(
            self,
            category,
            search_filter,
            kw,
            sort,
            page,
            my_id
    ):
        # 일단 검색 조건을 통해 post를 가져옴.
        posts = get_posts_from_db(category, search_filter, kw, sort, None)

        # 특정 사용자가 좋아요를 누른 Post ID들을 가져옴
        liked_post_ids = Like.objects.filter(user_id=my_id).values_list('post_id', flat=True)

        # 검색 조건에 맞는 게시물 중 사용자가 좋아요를 누른 게시물만 필터링
        liked_posts = posts.filter(id__in=liked_post_ids)

        pagination = Paginator(liked_posts, POST_LIST_PAGE_SIZE)
        page_obj = pagination.page(page).object_list
        list_size = len(page_obj)

        post_serializer = PostListSerializer(page_obj, many=True)
        return {"status": status.HTTP_200_OK,
                "message": "post list successfully",
                "data": {"page": page,  # 현재 페이지
                         "page_size": POST_LIST_PAGE_SIZE,  # 한페이지당 게시글 개수
                         "total_page_count": (liked_posts.count() + POST_LIST_PAGE_SIZE - 1) // POST_LIST_PAGE_SIZE,
                         "list_size": list_size,  # 게시글 개수
                         "post_list": post_serializer.data,
                         }}


class PostService:
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def update_hit(self, request, post, response):
        # 사용자 IP 주소 가져오기
        ip_address = self.get_client_ip(request)
        cache_key = f'viewed_article_{post.id}_{ip_address}'

        # 마지막 조회 시간 가져오기
        last_viewed = cache.get(cache_key)
        should_update = False

        if not last_viewed:
            should_update = True
        else:
            last_viewed_time = timezone.datetime.strptime(last_viewed, "%Y-%m-%d %H:%M:%S.%f")
            last_viewed_time = timezone.make_aware(last_viewed_time, timezone.get_default_timezone())
            if timezone.now() - last_viewed_time > timedelta(minutes=1):
                should_update = True

        if should_update:
            post.views += 1
            post.save()
            response.data["data"]["views"] += 1
            cache.set(cache_key, timezone.now().strftime("%Y-%m-%d %H:%M:%S.%f"), timeout=60)

        return response

    def get_client_ip(self, request):
        """Get the client IP address from the request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def retrieve_post(self, post_id):
        """
            <설명>
            - post_id를 받아서 select 후 알맞은 file model instances와 같이 return 한다.
            - 만약 post_id 가 없을 시 DoesNotExist을 발생시킨다.
        """

        post = get_post_instance(post_id)

        serializer = PostRetrieveSerializer(post)
        # view 함수로 넘겨주기
        return post, {"status": status.HTTP_200_OK,
                      "message": "post retrieve successfully",
                      "data": serializer.data,
                      }

    def create_post(
            self,
            category,
            title,
            content,
            html_content,
            author,
            files=None
    ):
        """
            <설명>
                - post를 생성할때 쓰인다.
                - files 와 post에 필요한 form을 받아서 저장한다.
            <로직>
                1. service 단 validation -> category에 맞는 permision 확인
                2. post model 부분 분리 후 시리얼라이즈 유효성 검사
                3. 트랜잭션 단위 설정 후 post 저장
                4. file 부분 분리후 FileSerivce 인스턴스 생성
                5. file 부분 저장
        """

        # check_post_create_permission
        only_staff_can_create_post_notice(category=category, author=author)

        # request.data 로 부터 post model 분리
        post_data = {'category': category,
                     'html_content': html_content,
                     'content': content,
                     'title': title,
                     'author': author.id
                     }
        post_serializer = PostCreateSerializer(data=post_data)
        if not post_serializer.is_valid():
            raise exceptions.ValidationError(post_serializer.errors)

        # 트랜잭션 처리
        with transaction.atomic():
            post = post_serializer.save()

            # file 생성
            if files:
                instance = FileService()
                instance.create_files(files, post)
            return {"message": "Resource created successfully", "status_code": status.HTTP_201_CREATED}

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

        post = get_post_instance(post_id)

        with transaction.atomic():
            instance = FileService()
            instance.delete_files(post)  # file 삭제
            post.delete()  # post 삭제
            return {"message": "Resource deleted successfully", "status_code": status.HTTP_204_NO_CONTENT}

    def update_post(
            self,
            post_id,
            category=None,
            title=None,
            content=None,
            html_content=None,
            files=None,
            files_state=None,
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
                5. files_state에 따라 file 부분 수정 혹은 삭제
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

        # 해당 post 가져옴
        post = get_post_instance(post_id)

        # 직렬화
        post_serializer = PostCreateSerializer(post, data=post_data_for_serialize, partial=True)
        if not post_serializer.is_valid():
            raise exceptions.ValidationError(post_serializer.errors)

        with transaction.atomic():
            post = post_serializer.save()

            # file 수정 또는 삭제
            if files_state:
                instance = FileService()
                if files_state == PostFilesState.REPLACE and files is not None:
                    instance.put_files(files, post)
                elif files_state == PostFilesState.DELETE:
                    instance.delete_files(post)
                else:
                    return {"message": "files_state is wrong", "status_code": status.HTTP_400_BAD_REQUEST}
            return {"message": "Resource updated successfully", "status_code": status.HTTP_200_OK}
