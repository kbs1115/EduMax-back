import pytest
from django.http import QueryDict
from rest_framework import status
from rest_framework.serializers import ModelSerializer, BaseSerializer

from community.service.file_service import FileService
from community.service.like_service import LikeService
from community.view.comment_view import CommentView
from community.service.comment_service import CommentService

"""
Mocking을 위한 fixture가 있다.

"""


@pytest.fixture
def mocked_s3_upload_file(mocker):
    return mocker.patch.object(FileService, "s3_upload_file")


@pytest.fixture
def mocked_s3_delete_file(mocker):
    return mocker.patch.object(FileService, "s3_delete_file")


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
def mocked_get_comment_user_id(mocker):
    return mocker.patch("community.service.comment_service.get_comment_user_id")


@pytest.fixture
def mocked_get_post_from_id(mocker):
    return mocker.patch(
        "community.service.comment_service.get_post_from_id",
        return_value=mocker.Mock(id=1),
    )


@pytest.fixture
def mocked_function_check_like_inst_exist_with_post_id(mocker):
    return mocker.patch(
        "community.view.like_view.check_like_inst_exist_with_post_id",
        return_value=False
    )


@pytest.fixture
def mocked_function_check_like_inst_exist_with_post_id_if_exist(mocker):
    return mocker.patch(
        "community.view.like_view.check_like_inst_exist_with_post_id",
        return_value=True
    )


@pytest.fixture
def mocked_function_check_like_inst_exist_with_comment_id(mocker):
    return mocker.patch(
        "community.view.like_view.check_like_inst_exist_with_comment_id",
        return_value=False
    )


@pytest.fixture
def mocked_function_check_like_inst_exist_with_comment_id_if_exist(mocker):
    return mocker.patch(
        "community.view.like_view.check_like_inst_exist_with_comment_id",
        return_value=True
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
def mocked_get_lecture_from_id(mocker):
    mocked_lecture = mocker.patch(
        "community.service.lecture_service.get_lecture_from_id"
    )
    mocked_lecture.return_value = mocker.Mock()
    return mocked_lecture


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
def mocked_lecture_list_serializer(mocker):
    mocked_serializer = mocker.Mock(data="data")
    mocker.patch(
        "community.service.lecture_service.LectureListSerializer",
        return_value=mocked_serializer,
    )
    return mocked_serializer


@pytest.fixture
def mocked_lecture_retrieve_serializer(mocker):
    mocked_serializer = mocker.Mock(data="data")
    mocker.patch(
        "community.service.lecture_service.LectureRetrieveSerializer",
        return_value=mocked_serializer,
    )
    return mocked_serializer


@pytest.fixture
def mocked_lecture_create_serializer(mocker):
    mocked_serializer = mocker.Mock(data="data")
    mocker.patch(
        "community.service.lecture_service.LectureCreateSerializer",
        return_value=mocked_serializer,
    )
    return mocked_serializer


@pytest.fixture
def mocked_get_request(mocker):
    return mocker.Mock()


@pytest.fixture
def mocked_create_comment(mocker):
    return mocker.patch.object(CommentService, "create_comment")


@pytest.fixture
def mocked_get_comment(mocker):
    return mocker.patch.object(CommentService, "get_comment")


@pytest.fixture
def mocked_update_comment(mocker):
    return mocker.patch.object(CommentService, "update_comment")


@pytest.fixture
def mocked_delete_comment(mocker):
    return mocker.patch.object(CommentService, "delete_comment")


@pytest.fixture
def mocked_check_object_permissions(mocker):
    return mocker.patch.object(CommentView, "check_object_permissions")


@pytest.fixture
def mocked_check_object_permissions(mocker):
    return mocker.patch.object(CommentView, "check_object_permissions")


@pytest.fixture
def mocked_post_request(user_instance, mocker):
    query_dict = QueryDict("files=test1.txt&files=test2.txt&files=test3.txt")
    return mocker.Mock(user=user_instance, FILES=query_dict)


@pytest.fixture
def mocked_request(user_instance, mocker):
    return mocker.Mock(user=user_instance)


@pytest.fixture
def mocked_get_lectures_with_category(search_lecture_instances, mocker):
    mocked_func = mocker.patch(
        "community.service.lecture_service.get_lectures_with_category"
    )
    mocked_func.return_value = search_lecture_instances
    return mocked_func


@pytest.fixture
def mocked_search_lectures_with_filter(search_lecture_instances, mocker):
    mocked_func = mocker.patch(
        "community.service.lecture_service.search_lectures_with_filter"
    )
    mocked_func.return_value = search_lecture_instances
    return mocked_func


@pytest.fixture
def mocked_method_generate_like(mocker):
    mocker = mocker.patch.object(LikeService, "generate_like")
    mocker.return_value = {
        "message": "LIKE created successfully",
        "status_code": status.HTTP_201_CREATED
    }
    return mocker


@pytest.fixture
def mocked_serializer_save(mocker):
    return mocker.patch.object(ModelSerializer, "save")


@pytest.fixture
def mocked_is_valid(mocker):
    return mocker.patch.object(BaseSerializer, "is_valid")
