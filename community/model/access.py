from rest_framework.exceptions import NotFound, ValidationError
from django.db.models import Q

from community.model.models import Post, Comment, Lecture
from edumax_account.models import User
from community.domain.definition import (
    TREE_STRUCTURE,
    LectureCategoriesDepth1Param,
    LectureCategoriesDepth2Param,
    LectureCategoriesDepth3Param,
    LectureCategoriesDepth4Param,
)
from community.domain.definition import LectureSearchFilterParam


def get_post_from_id(id):
    try:
        instance = Post.objects.get(pk=id)
        return instance
    except Post.DoesNotExist:
        raise NotFound("Post does not exists")


def get_parent_post_id(comment_id):
    try:
        comment = Comment.objects.get(pk=comment_id)
        return comment.post.id
    except Comment.DoesNotExist:
        raise NotFound("Parent Comment does not exists")


def get_comment_user_id(comment_id):
    try:
        comment = Comment.objects.get(pk=comment_id)
        return comment.author.id
    except Comment.DoesNotExist:
        raise NotFound("Comment not found")


def get_comment_from_id(comment_id):
    try:
        comment = Comment.objects.get(pk=comment_id)
        return comment
    except Comment.DoesNotExist:
        raise NotFound("comment not found")


def get_lectures_with_category(category):
    if category in LectureCategoriesDepth1Param:
        lectures = Lecture.objects.filter(category_d1=category).all()
    elif category in LectureCategoriesDepth2Param:
        lectures = Lecture.objects.filter(category_d2=category).all()
    elif category in LectureCategoriesDepth3Param:
        lectures = Lecture.objects.filter(category_d3=category).all()
    elif category in LectureCategoriesDepth4Param:
        lectures = Lecture.objects.filter(category_d4=category).all()
    else:
        raise ValidationError("Invalid category")

    return lectures


def get_lecture_from_id(lecture_id):
    try:
        instance = Lecture.objects.get(pk=lecture_id)
        return instance
    except Lecture.DoesNotExist:
        raise NotFound("Post does not exists")


def get_lecture_user_id(lecture_id):
    try:
        instance = Lecture.objects.get(pk=lecture_id)
        return instance.author.id
    except Lecture.DoesNotExist:
        raise NotFound("Lecture does not exists")
    except User.DoesNotExist:
        raise NotFound("Author not found")


def search_lectures_with_filter(lectures, kw, search_filter):
    # 검색 + 최신순 정렬 수행
    if kw and search_filter == LectureSearchFilterParam.TOTAL:
        lectures = lectures.filter(
            Q(author__nickname__icontains=kw) | Q(title__icontains=kw)
        ).distinct()
    elif kw and search_filter == LectureSearchFilterParam.AUTHOR:
        lectures = lectures.filter(Q(author__nickname__icontains=kw))
    elif kw and search_filter == LectureSearchFilterParam.TITLE:
        lectures = lectures.filter(Q(title__icontains=kw))

    if lectures:
        lectures = lectures.order_by("-created_at")

    return lectures
