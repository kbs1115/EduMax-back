import pytest
from datetime import datetime
from django.db.models import QuerySet

from account.models import User
from community.model.models import Comment, Post, File, Lecture, Like
from community.domain.definition import PostCategories

"""
Unit test에 사용되는 model instance를 정의함.
"""


@pytest.fixture
def make_user_instance():
    def _make_user_instance(number):
        return [
            User(
                id=i + 1,
                login_id=f"test{i}",
                email=f"test{i}@testemail.com",
                nickname=f"testuser{i}",
                password="pwpwpwpw",
            )
            for i in range(number)
        ]

    return _make_user_instance


@pytest.fixture
def make_post_instance():
    def _make_post_instance(number, category, user):
        return [
            Post(
                id=i + 1,
                title=f"test{i}",
                content=f"test_content{i}",
                html_content="test_htmlcontent",
                category=category,
                author=user,
            )
            for i in range(number)
        ]

    return _make_post_instance


@pytest.fixture
def make_comment_instance():
    def _make_comment_instance(number, user, post, parent):
        return [
            Comment(
                id=i + 1,
                content=f"testcontent{i}",
                html_content="html_testcontent",
                author=user,
                post=post,
                parent_comment=parent,
            )
            for i in range(number)
        ]

    return _make_comment_instance


@pytest.fixture
def make_lecture_instance():
    def _make_lecture_instance(startid, number, user, c1, c2, c3, c4):
        return [
            Lecture(
                id=i + 1,
                title=f"test{i}",
                youtube_id=f"youtube{i}",
                author=user,
                category_d1=c1,
                category_d2=c2,
                category_d3=c3,
                category_d4=c4,
                created_at=datetime(2024, 2, 14, 0, 0, i),
            )
            for i in range(startid, startid + number)
        ]

    return _make_lecture_instance


@pytest.fixture
def user_instance(make_user_instance):
    return make_user_instance(1)[0]


@pytest.fixture
def post_instance(user_instance, make_post_instance):
    return make_post_instance(1, PostCategories.FREE, user_instance)[0]


@pytest.fixture
def comment_instance(user_instance, post_instance, make_comment_instance):
    return make_comment_instance(1, user_instance, post_instance, None)[0]


@pytest.fixture
def file_instance(comment_instance):
    file = File(file_location="filelocation", post=None, comment=comment_instance)
    return file


@pytest.fixture
def like_comment_instance(comment_instance, user_instance):
    like = Like(comment=comment_instance, post=None, user=user_instance)
    return like


@pytest.fixture
def like_post_instance(post_instance, user_instance):
    like = Like(comment=None, post=post_instance, user=user_instance)
    return like


@pytest.fixture
def lecture_instances(user_instance, make_lecture_instance):
    lecture1 = make_lecture_instance(0, 1, user_instance, "KO", None, None, None)
    lecture2 = make_lecture_instance(1, 1, user_instance, "EN", None, None, None)
    return lecture1 + lecture2


@pytest.fixture
def search_lecture_instances(make_user_instance, make_lecture_instance):
    users = make_user_instance(2)
    lectureEN1 = make_lecture_instance(0, 10, users[0], "EN", None, None, None)
    lectureEN2 = make_lecture_instance(10, 10, users[1], "EN", None, None, None)

    ret = lectureEN1 + lectureEN2

    queryset = QuerySet(model=Lecture)
    queryset._result_cache = [inst for inst in ret]

    return queryset
