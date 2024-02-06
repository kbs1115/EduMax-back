import pytest, tempfile
import io
from rest_framework.test import APIClient
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from PIL import Image

from account.models import User
from community.model.models import Post, Comment, File
from community.domain.definition import PostCategories
from community.service.file_service import FileService


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def logined_client():
    client = APIClient()
    client2 = APIClient()
    user = User(
        id=1,
        login_id="kbs1115",
        email="bruce1115@naver.com",
        nickname="KKKBBBSSS",
        password="pwpwpwpw",
    )
    user.save()
    user2 = User(
        id=2,
        login_id="testuser1",
        email="test@naver.com",
        nickname="Testuser1",
        password="pwpwpwpw",
    )
    user2.save()
    token = TokenObtainPairSerializer.get_token(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")
    token = TokenObtainPairSerializer.get_token(user2)
    client2.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")

    return [client, client2]


@pytest.fixture
def setup_files():
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
        image = Image.new("RGB", (100, 100), "#ddd")
        image.save(tmp_file)

    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_file2:
        image = Image.new("RGB", (100, 100), color="blue")
        image.save(tmp_file2)

    return [tmp_file, tmp_file2]


@pytest.fixture
def setup_data():
    user1 = User.objects.get(id=1)
    user2 = User.objects.get(id=2)
    post1 = Post(
        id=1,
        title="user1's testpost",
        content="test1",
        html_content="htmltest1",
        category=PostCategories.FREE,
        author=user1,
    )
    post2 = Post(
        id=2,
        title="user2's testpost",
        content="test2",
        html_content="htmltest2",
        category=PostCategories.FREE,
        author=user2,
    )
    post1.save()
    post2.save()

    comment1 = Comment(
        id=1,
        content="testcomment1",
        html_content="htmltestcomment1",
        author=user2,
        post=post1,
        parent_comment=None,
    )
    comment1.save()
    comment2 = Comment(
        id=2,
        content="testcomment2",
        html_content="htmltestcomment2",
        author=user1,
        post=post1,
        parent_comment=None,
    )
    comment2.save()

    return [post1, post2, comment1, comment2, user1, user2]


@pytest.fixture
def validated_create_comment_request_body(mocker):
    return mocker.Mock(content="testcontent", html_content="testhtmlcontent")


@pytest.fixture
def mocked_s3_upload_file(mocker):
    return mocker.patch.object(FileService, "s3_upload_file")


@pytest.fixture
def mocked_s3_delete_file(mocker):
    return mocker.patch.object(FileService, "s3_delete_file")


@pytest.fixture
def save_file_model(setup_data):
    file1 = File(
        id=1,
        file_location="testlocation1",
        post=None,
        comment=setup_data[3],
    )
    file1.save()
    return file1
