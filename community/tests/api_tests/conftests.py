import pytest, tempfile
import io
from rest_framework.test import APIClient
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from PIL import Image

from edumax_account.models import User
from community.model.models import Post, Comment, File
from community.domain.definition import PostCategories, PostCategoriesParam
from community.serializers import PostCreateSerializer
from community.service.file_service import FileService


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def logined_client():
    client = APIClient()
    client2 = APIClient()
    client3 = APIClient()
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
    staff_user = User(
        id=3,
        login_id="testuser2",
        email="test2@naver.com",
        nickname="Testuser2",
        password="pwpwpwpw",
        is_staff=True,
    )
    staff_user.save()

    token = TokenObtainPairSerializer.get_token(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")
    token = TokenObtainPairSerializer.get_token(user2)
    client2.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")
    token = TokenObtainPairSerializer.get_token(staff_user)
    client2.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")
    return [client, client2, client3]


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

    # comment1 = Comment(
    #     id=1,
    #     content="testcomment1",
    #     html_content="htmltestcomment1",
    #     author=user2,
    #     post=post1
    # )
    # comment1.save()
    # comment2 = Comment(
    #     id=2,
    #     content="testcomment2",
    #     html_content="htmltestcomment2",
    #     author=user1,
    #     post=post1,
    # )
    # comment2.save()

    return [post1, post2, user1, user2]


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


@pytest.fixture
def save_file_model_fk_post(setup_data):
    file1 = File(
        id=2,
        file_location="testlocation2",
        post=setup_data[0],
        comment=None,
    )
    file1.save()
    return file1


@pytest.fixture
def create_staff_user_instance():
    staff_user = User(
        id=2,
        login_id="kbs1115",
        email="bruce1115@naver.com",
        nickname="KKKBBBSSS",
        password="pwpwpwpw",
        is_staff=True,
    )
    staff_user.save()
    return staff_user
