from typing import Type
import pytest
from PIL import Image
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import QuerySet
from django.utils.datastructures import MultiValueDict
from rest_framework import status

from account.models import User

from community.domain.definition import PostFilesState, PostCategoriesParam, PostSearchFilterParam, \
    PostSortCategoryParam
from community.model.models import Post, File
from community.serializers import PostCreateSerializer, PostListSerializer
from community.service.file_service import FileService
from community.view.validation import PostQueryParam, CreatePostRequestBody, UpdatePostRequestBody


# 팩토리 함수
def queryset_factory(model_class, instances=None):
    if instances:
        queryset = QuerySet(model=model_class)
        queryset._result_cache = [inst for inst in instances]
        return queryset
    else:
        return model_class.objects.none()


# 모델 인스턴스, 각종 django request
@pytest.fixture
def files_form_of_request_dot_files():
    image1 = Image.new('RGB', (100, 100), color='red')
    image2 = Image.new('RGB', (100, 100), color='blue')

    buffer1 = io.BytesIO()
    buffer2 = io.BytesIO()
    image1.save(buffer1, format='PNG')
    image2.save(buffer2, format='PNG')

    image1_content = buffer1.getvalue()
    image2_content = buffer2.getvalue()

    uploaded_image1 = InMemoryUploadedFile(
        file=io.BytesIO(image1_content),
        field_name='files',
        name='image1.png',
        content_type='image/png',
        size=len(image1_content),
        charset='utf-8'
    )

    uploaded_image2 = InMemoryUploadedFile(
        file=io.BytesIO(image2_content),
        field_name='files',
        name='image2.png',
        content_type='image/png',
        size=len(image2_content),
        charset='utf-8'
    )

    # request.Files와 같은 format
    return MultiValueDict({'files': [uploaded_image1, uploaded_image2]})


@pytest.fixture
def super_user_instance():
    superuser = User(
        id=1,
        login_id="kbs1115",
        email="bruce1115@naver.com",
        nickname="KKKBBBSSS",
        password="pwpwpwpw",
        is_superuser=True
    )
    return superuser


@pytest.fixture
def staff_user_instance():
    staff_user = User(
        id=2,
        login_id="kbs1115",
        email="bruce1115@naver.com",
        nickname="KKKBBBSSS",
        password="pwpwpwpw",
        is_staff=True
    )
    return staff_user


@pytest.fixture
def common_user_instance():
    user = User(
        id=3,
        login_id="kbs1115",
        email="bruce1115@naver.com",
        nickname="KKKBBBSSS",
        password="pwpwpwpw",
    )
    return user


@pytest.fixture
def valid_file_instance_list(valid_post_instance_list):
    return [
        File(
            id=1,
            post=valid_post_instance_list[0],
            file_location="test_location1"
        ), File(
            id=2,
            post=valid_post_instance_list[0],
            file_location="test_location2"
        )
    ]


@pytest.fixture
def valid_post_instance_list(common_user_instance):
    return [
        Post(
            id=1,
            title="test1",
            content="test1",
            html_content="test1",
            category="EQ",
            author=common_user_instance
        ), Post(
            id=2,
            title="test2",
            content="test2",
            html_content="test2",
            category="EQ",
            author=common_user_instance
        )
    ]


# service layer 메소드 모킹

@pytest.fixture
def mocked_delete_files_method(mocker):
    mocker = mocker.patch.object(FileService, 'delete_files')
    return mocker


@pytest.fixture
def mocked_create_files_method(mocker):
    mocker = mocker.patch.object(FileService, 'create_files')
    return mocker


@pytest.fixture
def mocked_update_files_method(mocker):
    mocker = mocker.patch.object(FileService, 'put_files')
    return mocker


@pytest.fixture
def mocked_s3_upload_file_method(mocker):
    mocker = mocker.patch.object(FileService, 's3_upload_file')
    return mocker


@pytest.fixture
def mocked_s3_delete_file_method(mocker):
    mocker = mocker.patch.object(FileService, 's3_delete_file')
    return mocker


# service layer 메소드 모킹- orm

@pytest.fixture
def mocked_get_files_id_list(mocker):
    mocker = mocker.patch.object(FileService, "get_files_id_list")
    mocker.return_value = [1, 2, 3]
    return mocker


@pytest.fixture
def mocked_get_file_instance(mocker, valid_file_instance_list):
    mocker = mocker.patch.object(FileService, "get_file_instance")
    mocker.return_value = valid_file_instance_list[0]
    return mocker


@pytest.fixture
def mocked_get_post_obj(mocker, valid_post_instance_list):
    mocker = mocker.patch("community.service.post_service.get_post_instance",
                          return_value=valid_post_instance_list[0])

    return mocker


@pytest.fixture
def mocked_function_get_post_user_id(mocker):
    mocker = mocker.patch("community.view.post_view.get_post_user_id", return_value=1)
    return mocker


@pytest.fixture
def mocked_function_get_posts_from_db_return_queryset(mocker, valid_post_instance_list):
    mocked_posts = queryset_factory(Post, valid_post_instance_list)
    mocker = mocker.patch("community.service.post_service.get_posts_from_db", return_value=mocked_posts)

    return mocker


@pytest.fixture
def mocked_function_get_posts_from_db_return_empty_queryset(mocker, valid_post_instance_list):
    mocked_posts = queryset_factory(Post)
    mocker = mocker.patch("community.service.post_service.get_posts_from_db", return_value=mocked_posts)

    return mocker


@pytest.fixture
def mocked_serializer_method_get_likes_count(mocker):
    mocker = mocker.patch.object(PostListSerializer, "get_likes_count")
    mocker.return_value = 3
    return mocker


# 테스트용 각종 파라매터
@pytest.fixture
def valid_post_path_param():
    return 1


@pytest.fixture
def invalid_post_path_param_list():
    return [-1, 0, 'asdzxc']


@pytest.fixture
def mocked_service_response():
    return {"status": status.HTTP_200_OK,
            "message": "mocked_message",
            "data": 'mocked_data',
            }


@pytest.fixture
def valid_post_query_params_list():
    return [{
        f'{PostQueryParam.PAGE}': 1,
        f'{PostQueryParam.CATEGORY}': PostCategoriesParam.NOTICE,
        f'{PostQueryParam.Q}': 'hello',
        f'{PostQueryParam.SEARCH_FILTER}': PostSearchFilterParam.AUTHOR,
    }, {
        f'{PostQueryParam.PAGE}': 1,
        f'{PostQueryParam.CATEGORY}': PostCategoriesParam.NOTICE,
        f'{PostQueryParam.SORT}': PostSortCategoryParam.CREATED_AT,
        f'{PostQueryParam.SEARCH_FILTER}': PostSearchFilterParam.AUTHOR,
    }, {
        f'{PostQueryParam.PAGE}': 1,
        f'{PostQueryParam.Q}': 'hello',
        f'{PostQueryParam.SORT}': PostSortCategoryParam.CREATED_AT,
        f'{PostQueryParam.SEARCH_FILTER}': PostSearchFilterParam.AUTHOR,
    }, {
        f'{PostQueryParam.CATEGORY}': PostCategoriesParam.NOTICE,
        f'{PostQueryParam.Q}': 'hello',
        f'{PostQueryParam.SORT}': PostSortCategoryParam.CREATED_AT,
        f'{PostQueryParam.SEARCH_FILTER}': PostSearchFilterParam.AUTHOR,
    }, {
        f'{PostQueryParam.PAGE}': 1,
        f'{PostQueryParam.CATEGORY}': PostCategoriesParam.NOTICE,
        f'{PostQueryParam.Q}': 'hello',
        f'{PostQueryParam.SORT}': PostSortCategoryParam.CREATED_AT,
        f'{PostQueryParam.SEARCH_FILTER}': PostSearchFilterParam.AUTHOR,
    }]


@pytest.fixture
def invalid_post_query_params_list():
    return [
        {
            # sort invalid
            f'{PostQueryParam.PAGE}': 1,
            f'{PostQueryParam.CATEGORY}': PostCategoriesParam.NOTICE,
            f'{PostQueryParam.Q}': 'hello',
            f'{PostQueryParam.SORT}': 'CREAT',
            f'{PostQueryParam.SEARCH_FILTER}': PostSearchFilterParam.AUTHOR,
        }, {
            # search_filter invalid
            f'{PostQueryParam.PAGE}': 1,
            f'{PostQueryParam.CATEGORY}': PostCategoriesParam.NOTICE,
            f'{PostQueryParam.Q}': 'hello',
            f'{PostQueryParam.SORT}': PostSortCategoryParam.CREATED_AT,
            f'{PostQueryParam.SEARCH_FILTER}': 'AUT',
        }, {
            # category invalid
            f'{PostQueryParam.PAGE}': 1,
            f'{PostQueryParam.CATEGORY}': 'N',
            f'{PostQueryParam.Q}': 'hello',
            f'{PostQueryParam.SORT}': PostSortCategoryParam.CREATED_AT,
            f'{PostQueryParam.SEARCH_FILTER}': PostSearchFilterParam.AUTHOR,
        }, {
            # page invalid
            # 900만 이런거 넣어버리면 캐치못함 -> validator에 추가 필요
            f'{PostQueryParam.PAGE}': -1,
            f'{PostQueryParam.CATEGORY}': PostCategoriesParam.NOTICE,
            f'{PostQueryParam.Q}': 'hello',
            f'{PostQueryParam.SORT}': PostSortCategoryParam.CREATED_AT,
            f'{PostQueryParam.SEARCH_FILTER}': PostSearchFilterParam.AUTHOR,
        }
    ]


@pytest.fixture
def valid_reqeust_post_body_for_method_post():
    return [{
        f"{CreatePostRequestBody.CATEGORY}": PostCategoriesParam.NOTICE,
        f"{CreatePostRequestBody.TITLE}": "HELLO",
        f"{CreatePostRequestBody.HTML_CONTENT}": "<P>ASDASD</P>>",
        f"{CreatePostRequestBody.CONTENT}": "ASD",
    }]


@pytest.fixture
def invalid_reqeust_post_body_for_method_post():
    return [{
        f"{CreatePostRequestBody.CATEGORY}": "N",
        f"{CreatePostRequestBody.TITLE}": "HELLO",
        f"{CreatePostRequestBody.HTML_CONTENT}": "<P>ASDASD</P>>",
        f"{CreatePostRequestBody.CONTENT}": "ASD",
    }, {
        f"{CreatePostRequestBody.CATEGORY}": PostCategoriesParam.NOTICE,
        f"{CreatePostRequestBody.TITLE}": "0123456789012345678901234567890",  # MAX_LENGTH 30 초과
        f"{CreatePostRequestBody.HTML_CONTENT}": "<P>ASDASD</P>>",
        f"{CreatePostRequestBody.CONTENT}": "ASD",
    }, {
        f"{CreatePostRequestBody.CATEGORY}": PostCategoriesParam.NOTICE,
        f"{CreatePostRequestBody.TITLE}": "HELLO",
        f"{CreatePostRequestBody.HTML_CONTENT}": "",
        f"{CreatePostRequestBody.CONTENT}": "ASD",
    }, {
        f"{CreatePostRequestBody.CATEGORY}": PostCategoriesParam.NOTICE,
        f"{CreatePostRequestBody.TITLE}": "HELLO",
        f"{CreatePostRequestBody.HTML_CONTENT}": "",
        f"{CreatePostRequestBody.CONTENT}": "",
    }, ]


@pytest.fixture
def valid_reqeust_post_body_for_method_patch():
    return [{
        f"{UpdatePostRequestBody.CATEGORY}": PostCategoriesParam.NOTICE,
        f"{UpdatePostRequestBody.CONTENT}": "ASDAS",
        f"{UpdatePostRequestBody.TITLE}": "ASDAS",
        f"{UpdatePostRequestBody.HTML_CONTENT}": "ASDAS",
        f"{UpdatePostRequestBody.FILES_STATE}": PostFilesState.REPLACE,
    }, {
        f"{UpdatePostRequestBody.CATEGORY}": PostCategoriesParam.NOTICE,
        f"{UpdatePostRequestBody.CONTENT}": "ASDAS",
        f"{UpdatePostRequestBody.TITLE}": "ASDAS",
        f"{UpdatePostRequestBody.HTML_CONTENT}": "ASDAS",
        f"{UpdatePostRequestBody.FILES_STATE}": PostFilesState.DELETE,
    }, {
        f"{UpdatePostRequestBody.CATEGORY}": PostCategoriesParam.NOTICE,
        f"{UpdatePostRequestBody.CONTENT}": "ASDAS",
        f"{UpdatePostRequestBody.TITLE}": "ASDAS",
        f"{UpdatePostRequestBody.HTML_CONTENT}": "ASDAS"
    }, {
        f"{UpdatePostRequestBody.CATEGORY}": PostCategoriesParam.NOTICE,
        f"{UpdatePostRequestBody.CONTENT}": "ASDAS",
        f"{UpdatePostRequestBody.TITLE}": "ASDAS",
        f"{UpdatePostRequestBody.HTML_CONTENT}": "ASDAS",
        f"{UpdatePostRequestBody.FILES_STATE}": PostFilesState.REPLACE,
    }, ]


@pytest.fixture
def invalid_reqeust_post_body_for_method_patch():
    return [{
        # CATEGORY 에러
        f"{UpdatePostRequestBody.CATEGORY}": "N",
        f"{UpdatePostRequestBody.CONTENT}": "ASDAS",
        f"{UpdatePostRequestBody.TITLE}": "ASDAS",
        f"{UpdatePostRequestBody.HTML_CONTENT}": "ASDAS",
        f"{UpdatePostRequestBody.FILES_STATE}": PostFilesState.REPLACE,
    }, {
        # FILES_STATE 에러
        f"{UpdatePostRequestBody.CATEGORY}": PostCategoriesParam.NOTICE,
        f"{UpdatePostRequestBody.CONTENT}": "ASDAS",
        f"{UpdatePostRequestBody.TITLE}": "ASDAS",
        f"{UpdatePostRequestBody.HTML_CONTENT}": "ASDAS",
        f"{UpdatePostRequestBody.FILES_STATE}": "ASDZXC",
    }, {
        # TITLE MAX_LENGTH 에러
        f"{UpdatePostRequestBody.CATEGORY}": PostCategoriesParam.NOTICE,
        f"{UpdatePostRequestBody.CONTENT}": "ASDAS",
        f"{UpdatePostRequestBody.TITLE}": "0123456789012345678901234567890",  # MAX_LENGTH 30 초과,
        f"{UpdatePostRequestBody.HTML_CONTENT}": "ASDAS",
        f"{UpdatePostRequestBody.FILES_STATE}": "ASDZXC",
    }, {
        # CONTENT MIN_LENGTH 에러
        f"{UpdatePostRequestBody.CATEGORY}": PostCategoriesParam.NOTICE,
        f"{UpdatePostRequestBody.CONTENT}": "",
        f"{UpdatePostRequestBody.TITLE}": "0",
        f"{UpdatePostRequestBody.HTML_CONTENT}": "ASDAS",
        f"{UpdatePostRequestBody.FILES_STATE}": "ASDZXC",
    }, {
        # HTML CONTENT MIN_LENGTH 에러
        f"{UpdatePostRequestBody.CATEGORY}": PostCategoriesParam.NOTICE,
        f"{UpdatePostRequestBody.CONTENT}": "ASDAS",
        f"{UpdatePostRequestBody.TITLE}": "0",
        f"{UpdatePostRequestBody.HTML_CONTENT}": "",
        f"{UpdatePostRequestBody.FILES_STATE}": "ASDZXC",
    }, ]


# api test용 setup
@pytest.fixture
def set_up_create_posts(staff_user_instance):
    staff_user_instance.save()
    posts = []
    for category in PostCategoriesParam:
        cnt = 1
        while cnt < 21:
            posts.append({
                'id': cnt,
                'title': f'title{cnt}',
                'content': f'content{cnt}',
                'html_content': f'html_content{cnt}',
                'category': category.value,
                'author': staff_user_instance.id
            })
            cnt += 1
    serializer = PostCreateSerializer(many=True, data=posts)
    assert serializer.is_valid()
    serializer.save()
