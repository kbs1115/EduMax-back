import pytest

from community.service.lecture_service import LecturesService


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
