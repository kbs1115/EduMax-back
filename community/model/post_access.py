from django.db.models import Q, Count
from rest_framework import exceptions

from community.domain.definition import PostSearchFilterParam, PostSortCategoryParam
from community.model.models import Post


def get_posts_from_db(
        category,
        search_filter,
        kw,
        sort,
):
    # category와 무관하게 select 가능 추가
    if category == PostCategoriesParam.ALL:
        posts = Post.objects.all()

    else:  # category에 따른 select
        posts = Post.objects.filter(category=category).all()

    # kw에 따른 select
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

    return posts


def get_post_instance(post_id):
    try:
        return Post.objects.get(pk=post_id)

    # 해당 게시글이 존재하지않을 때
    except Post.DoesNotExist:
        raise exceptions.NotFound("post not found")


def get_post_user_id(post_id):
    try:
        post = Post.objects.get(pk=post_id)
        return post.author.id

    except Post.DoesNotExist:
        raise exceptions.NotFound("post not found")
