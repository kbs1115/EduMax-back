import pytest
from rest_framework.exceptions import ValidationError

from community.service.lecture_service import LecturesService, LectureService


class TestLecturesService:
    def test_get_lectures(
        self,
        valid_get_lectures_param_data,
        mocked_get_lectures_with_category,
        mocked_search_lectures_with_filter,
        mocked_lecture_list_serializer,
    ):
        response = LecturesService.get_lectures(**valid_get_lectures_param_data[0])

        assert response["status_code"] == 200
        assert response["data"]["list_size"] == 5
        assert response["data"]["page_size"] == 15
        assert response["data"]["page"] == 2
        assert response["data"]["post_list"] == mocked_lecture_list_serializer.data


class TestLectureService:
    def test_get_lecture(
        self, mocked_lecture_retrieve_serializer, mocked_get_lecture_from_id
    ):
        response = LectureService.get_lecture(1)

        assert response["status_code"] == 200
        assert response["data"] == mocked_lecture_retrieve_serializer.data

    def test_create_lecture(
        self, mocked_lecture_create_serializer, valid_create_lecture_data
    ):
        mocked_lecture_create_serializer.is_valid.return_value = True
        lecture_data = valid_create_lecture_data

        response = LectureService.create_lecture(**lecture_data)

        assert response["status_code"] == 201
        mocked_lecture_create_serializer.is_valid.assert_called_once()
        mocked_lecture_create_serializer.save.assert_called_once()

        mocked_lecture_create_serializer.is_valid.return_value = False

        with pytest.raises(ValidationError):
            LectureService.create_lecture(**lecture_data)

    def test_update_lecture(
        self,
        mocked_lecture_create_serializer,
        valid_create_lecture_data,
        mocked_get_lecture_from_id,
    ):
        mocked_lecture_create_serializer.is_valid.return_value = True
        valid_create_lecture_data["lecture_id"] = 1
        valid_create_lecture_data.pop("author")
        lecture_data = valid_create_lecture_data

        response = LectureService.update_lecture(**lecture_data)

        assert response["status_code"] == 200
        mocked_lecture_create_serializer.is_valid.assert_called_once()
        mocked_lecture_create_serializer.save.assert_called_once()
        mocked_get_lecture_from_id.assert_called_once()

        mocked_lecture_create_serializer.is_valid.return_value = False

        with pytest.raises(ValidationError):
            LectureService.update_lecture(**lecture_data)

    def test_delete_lecture(
        self,
        mocker,
        mocked_get_lecture_from_id,
    ):
        response = LectureService.delete_lecture(1)

        assert response["status_code"] == 204
        mocked_get_lecture_from_id.assert_called_once()
        mocked_get_lecture_from_id.return_value.delete.assert_called_once()
