from django.core.paginator import Paginator
from django.db.models import QuerySet
from rest_framework import exceptions

from community.domain.definition import POST_LIST_PAGE_SIZE
from community.service.post_service import PostService, PostsService
from community.tests.conftests import *

from community.models import Post


class TestGetPostsService:
    # 페이징처리, 직렬화 결과 테스트
    # 페이징처리 -posts가 빈 쿼리셋을 return 해도 돌아가는지
    # - posts개수를 넘기는 page를 입력했을때 걷어내야함
    # - 멀쩡한거 넘기면 잘 넘어가는지
    # 직렬화:
    # 잘 return 하는지
    def test_paging_with_invalid_page(
            self,
            mocker,
            valid_post_instance_list
    ):
        mocker = mocker.patch.object(PostsService, "get_posts_from_db")
        mocked_posts = queryset_factory(Post, valid_post_instance_list)
        mocker.return_value = mocked_posts

        invalid_page = len(valid_post_instance_list) + 1
        with pytest.raises(exceptions.NotFound):
            # page 제외 나머지 매개변수 안씀
            PostsService().get_posts(
                category=1,
                search_filter=1,
                kw=1,
                sort=1,
                page=invalid_page,
            )

    def test_paging_with_valid_page(
            self,
            mocker,
            valid_post_instance_list
    ):
        mocker = mocker.patch.object(PostsService, "get_posts_from_db")
        mocked_posts = queryset_factory(Post, valid_post_instance_list)
        mocker.return_value = mocked_posts

        page = 1
        # page 제외 나머지 매개변수 안씀
        response = PostsService().get_posts(
            category=1,
            search_filter=1,
            kw=1,
            sort=1,
            page=page,
        )
        assert response

    def test_paging_with_valid_page_and_no_post(
            self,
            mocker
    ):
        mocker = mocker.patch.object(PostsService, "get_posts_from_db")
        mocked_posts = queryset_factory(Post)
        mocker.return_value = mocked_posts

        page = 1
        # page 제외 나머지 매개변수 안씀
        response = PostsService().get_posts(
            category=1,
            search_filter=1,
            kw=1,
            sort=1,
            page=page,
        )
        assert response
