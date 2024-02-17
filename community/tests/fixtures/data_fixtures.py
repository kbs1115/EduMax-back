import pytest

from community.domain.definition import (
    PostFilesState,
    LectureCategoriesDepth1Param,
    LectureSearchFilterParam,
)

"""
Unit test에 사용되는 body data, mock request 등을 정의함.
"""


@pytest.fixture
def comment_db_setup(user_instance, post_instance, comment_instance, file_instance, like_comment_instance):
    return {
        "user_instance": user_instance,
        "post_instance": post_instance,
        "comment_instance": comment_instance,
        "file_instance": file_instance,
        "like_instance": like_comment_instance
    }


@pytest.fixture
def lecture_db_setup(user_instance, lecture_instances):
    return {
        "user_instance": user_instance,
        "lecture_instances": lecture_instances,
    }


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


@pytest.fixture
def valid_serialized_lecture_data(user_instance):
    return {
        "title": "title1",
        "youtube_id": "youtube1",
        "author": user_instance.id,
        "category_d1": "KO",
        "category_d2": None,
        "category_d3": None,
        "category_d4": None,
    }


@pytest.fixture
def invalid_serialized_lecture_data(user_instance):
    return {
        "title": "title1",
        "author": user_instance.id,
        "category_d1": "KO",
        "category_d2": None,
        "category_d3": None,
        "category_d4": None,
    }


@pytest.fixture
def validated_create_comment_request_body(mocker):
    return mocker.Mock(content="testcontent", html_content="testhtmlcontent")


@pytest.fixture
def validated_update_comment_request_body(mocker):
    return mocker.Mock(
        content="testcontent",
        html_content="testhtmlcontent",
        files_state=PostFilesState.REPLACE,
    )


@pytest.fixture
def valid_serialized_lecture_data(user_instance):
    return {
        "title": "title1",
        "youtube_id": "youtube1",
        "author": user_instance.id,
        "category_d1": "KO",
        "category_d2": None,
        "category_d3": None,
        "category_d4": None,
    }


@pytest.fixture
def valid_get_lectures_param_data():
    return [
        {
            "page": 2,
            "category": LectureCategoriesDepth1Param.ENGLISH,
            "search_filter": LectureSearchFilterParam.TOTAL,
            "kw": "test",
        },
        {
            "page": 1,
            "category": LectureCategoriesDepth1Param.ENGLISH,
            "search_filter": LectureSearchFilterParam.TITLE,
            "kw": "test1",
        },
        {
            "page": 1,
            "category": LectureCategoriesDepth1Param.ENGLISH,
            "search_filter": LectureSearchFilterParam.AUTHOR,
            "kw": "testuser5",
        },
    ]


@pytest.fixture
def valid_create_lecture_data(user_instance):
    return {
        "title": "title1",
        "youtube_id": "youtube1",
        "author": user_instance,
        "category_d1": "KO",
        "category_d2": None,
        "category_d3": None,
        "category_d4": None,
    }
