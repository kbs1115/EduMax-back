import status as status
from django.core.paginator import Paginator
from django.db.models import Q, Count
from community.models import Post
from community.serializers import PostSerializer
from community.service.define import PostSearchFilterParam, PostSortCategoryParam
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist


class PostService:
    """
        <설명>
        - post_id를 받아서 select 후 return 한다.
        - 만약 post_id 가 없을 시 DoesNotExist을 발생시킨다.
    """
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

    def create_post(self, **form):
        pass
        # form을 받아서 content,author, title의 경우는 저장을 하고
        # 만약 file 이 있다면 file 형태는지금 python obj로 되어있을것이고
        # 이걸 aws로 올리기전에 시리얼라이즈 한후에 올리고 그걸 저장한다음에
        # 저장된 위치를 따와서 file models의 url에 저장해야한다.
        # form이 잘 저장되었거나 file 이 잘 저장되었을 경우 201 status return
