import pytest
from rest_framework import status

from account.models import User

from community.domain.definition import PostFilesState, PostCategoriesParam, PostSearchFilterParam, \
    PostSortCategoryParam
from community.view.validation import PostQueryParam, CreatePostRequestBody, UpdatePostRequestBody


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
        id=1,
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
        id=1,
        login_id="kbs1115",
        email="bruce1115@naver.com",
        nickname="KKKBBBSSS",
        password="pwpwpwpw",
    )
    return user


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
