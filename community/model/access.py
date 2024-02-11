from rest_framework.exceptions import NotFound
from community.model.models import Post, Comment, Lecture
from account.models import User
from community.domain.definition import (
    TREE_STRUCTURE,
    LectureCategoriesDepth1Param,
    LectureCategoriesDepth2Param,
    LectureCategoriesDepth3Param,
    LectureCategoriesDepth4Param,
)


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
    try:
        if category in LectureCategoriesDepth1Param:
            lectures = Lecture.objects.filter(category_d1=category).all()
        elif category in LectureCategoriesDepth2Param:
            lectures = Lecture.objects.filter(category_d2=category).all()
        elif category in LectureCategoriesDepth3Param:
            lectures = Lecture.objects.filter(category_d3=category).all()
        elif category in LectureCategoriesDepth4Param:
            lectures = Lecture.objects.filter(category_d4=category).all()

        return lectures
    except Lecture.DoesNotExist:
        raise NotFound("Lecture does not exists")


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
        raise NotFound("Post does not exists")
    except User.DoesNotExist:
        raise NotFound("Author not found")
