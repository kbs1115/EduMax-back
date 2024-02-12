import pytest

from community.domain.definition import PostFilesState


"""
Unit test에 사용되는 body data, mock request 등을 정의함.
"""

@pytest.fixture
def comment_db_setup(user_instance, post_instance, comment_instance, file_instance):
    return {
        "user_instance": user_instance,
        "post_instance": post_instance,
        "comment_instance": comment_instance,
        "file_instance": file_instance,
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
def validated_create_comment_request_body(mocker):
    return mocker.Mock(content="testcontent", html_content="testhtmlcontent")


@pytest.fixture
def validated_update_comment_request_body(mocker):
    return mocker.Mock(
        content="testcontent",
        html_content="testhtmlcontent",
        files_state=PostFilesState.REPLACE,
    )