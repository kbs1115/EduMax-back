import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from account.models import User
from community.model.models import Comment, Post, File
from community.domain.definition import PostCategories
from community.service.comment_service import *


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def logined_client():
    client = APIClient()
    user = User(
        id=1,
        login_id="kbs1115",
        email="bruce1115@naver.com",
        nickname="KKKBBBSSS",
        password="pwpwpwpw",
    )
    user.save()
    user2 = User(id=2)
    user2.save()
    token = TokenObtainPairSerializer.get_token(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")

    return client


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


@pytest.fixture
def comment_db_setup(user_instance, post_instance, comment_instance, file_instance):
    return {
        "user_instance": user_instance,
        "post_instance": post_instance,
        "comment_instance": comment_instance,
        "file_instance": file_instance,
    }


@pytest.fixture
def mocked_get_comment_from_id(mocker, comment_instance):
    return mocker.patch(
        "community.service.comment_service.get_comment_from_id",
        return_value=comment_instance,
    )


@pytest.fixture
def mocked_get_parent_post_id(mocker):
    return mocker.patch("community.service.comment_service.get_parent_post_id")


@pytest.fixture
def mocked_get_post_from_id(mocker):
    return mocker.patch(
        "community.service.comment_service.get_post_from_id",
        return_value=mocker.Mock(id=1),
    )


@pytest.fixture
def mocked_create_files(mocker):
    return mocker.patch.object(FileService, "create_files")


@pytest.fixture
def mocked_put_files(mocker):
    return mocker.patch.object(FileService, "put_files")


@pytest.fixture
def mocked_delete_files(mocker):
    return mocker.patch.object(FileService, "delete_files")


@pytest.fixture
def mocked_comment_create_serializer(mocker):
    mocked_serializer = mocker.Mock()
    mocker.patch(
        "community.service.comment_service.CommentCreateSerializer",
        return_value=mocked_serializer,
    )
    return mocked_serializer


@pytest.fixture
def mocked_comment_retrieve_serializer(mocker):
    mocked_serializer = mocker.Mock()
    mocker.patch(
        "community.service.comment_service.CommentRetrieveSerializer",
        return_value=mocked_serializer,
    )
    return mocked_serializer


@pytest.fixture
def valid_serialized_comment_data(user_instance, post_instance):
    return [
        {
            "content": "testcontent",
            "html_content": "testhtmlcontent",
            "author": user_instance.id,
            "parent_comment": None,
            "post": post_instance.id,
        },
        {
            "content": "testcontent",
            "html_content": "testhtmlcontent",
            "author": user_instance.id,
            "parent_comment": 2,  # 없지만, is_valid 테스트용 임의의 정수
            "post": post_instance.id,
        },
    ]


@pytest.fixture
def invalid_serialized_comment_data(user_instance, post_instance):
    return [
        {
            "content": "testcontent",
            "author": user_instance.id,
            "parent_comment": None,
            "post": post_instance.id,
        },
        {
            "content": None,
            "html_content": "testhtmlcontent",
            "author": user_instance.id,
            "parent_comment": 2,  # 없지만, is_valid 테스트용 임의의 정수
            "post": post_instance.id,
        },
    ]
