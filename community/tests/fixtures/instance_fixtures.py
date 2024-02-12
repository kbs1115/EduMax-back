import pytest

from account.models import User
from community.model.models import Comment, Post, File
from community.domain.definition import PostCategories

"""
Unit test에 사용되는 model instance를 정의함.
"""

@pytest.fixture
def user_instance():
    user = User(
        id=1,
        login_id="kbs1115",
        email="bruce1115@naver.com",
        nickname="KKKBBBSSS",
        password="pwpwpwpw",
    )
    return user


@pytest.fixture
def post_instance(user_instance):
    post = Post(
        id=1,
        title="test",
        content="test_content",
        html_content="test_htmlcontent",
        category=PostCategories.FREE,
        author=user_instance,
    )
    return post


@pytest.fixture
def comment_instance(user_instance, post_instance):
    comment = Comment(
        id=1,
        content="testcontent",
        html_content="html_testcontent",
        author=user_instance,
        post=post_instance,
        parent_comment=None,
    )
    return comment


@pytest.fixture
def file_instance(comment_instance):
    file = File(file_location="filelocation", post=None, comment=comment_instance)
    return file