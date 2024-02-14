import rest_framework.status as status
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework.exceptions import ValidationError

from community.model.access import (
    get_lectures_with_category,
    get_lecture_from_id,
    get_lecture_user_id,
    search_lectures_with_filter,
)
from community.domain.definition import (
    LectureSearchFilterParam,
    POST_LIST_PAGE_SIZE,
)
from community.serializers import (
    LectureListSerializer,
    LectureRetrieveSerializer,
    LectureCreateSerializer,
)


class LecturesService:
    @classmethod
    def get_lectures(cls, category, search_filter, kw, page):
        lectures = get_lectures_with_category(category)

        search_lectures = search_lectures_with_filter(lectures, kw, search_filter)

        pagination = Paginator(search_lectures, POST_LIST_PAGE_SIZE)
        page_obj = pagination.page(page).object_list
        list_size = len(page_obj)

        lecture_serializer = LectureListSerializer(page_obj, many=True)
        return {
            "status_code": status.HTTP_200_OK,
            "message": "lecture list successfully",
            "data": {
                "page": page,  # 현재 페이지
                "page_size": POST_LIST_PAGE_SIZE,  # 한페이지당 게시글 개수
                "list_size": list_size,  # 게시글 개수
                "post_list": lecture_serializer.data,
            },
        }


class LectureService:
    @classmethod
    def get_lecture_user_id(cls, lecture_id):
        return get_lecture_user_id(lecture_id)

    @classmethod
    def get_lecture(cls, lecture_id):
        lecture = get_lecture_from_id(lecture_id)
        serializer = LectureRetrieveSerializer(lecture)

        return {
            "status_code": status.HTTP_200_OK,
            "message": "lecture retrieve successfully",
            "data": serializer.data,
        }

    @classmethod
    def create_lecture(
        cls,
        category_d1,
        category_d2,
        category_d3,
        category_d4,
        title,
        youtube_id,
        author,
    ):
        lecture_data = {
            "category_d1": category_d1,
            "category_d2": category_d2,
            "category_d3": category_d3,
            "category_d4": category_d4,
            "title": title,
            "youtube_id": youtube_id,
            "author": author.id,
        }

        serializer = LectureCreateSerializer(data=lecture_data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        serializer.save()

        return {
            "message": "Lecture created successfully",
            "status_code": status.HTTP_201_CREATED,
            "data": serializer.data,
        }

    @classmethod
    def update_lecture(
        cls,
        lecture_id,
        category_d1,
        category_d2,
        category_d3,
        category_d4,
        title,
        youtube_id,
    ):
        update_data = dict()
        update_data["category_d1"] = category_d1
        update_data["category_d2"] = category_d2
        update_data["category_d3"] = category_d3
        update_data["category_d4"] = category_d4
        if title:
            update_data["title"] = title
        if youtube_id:
            update_data["youtube_id"] = youtube_id

        lecture = get_lecture_from_id(lecture_id)
        update_serializer = LectureCreateSerializer(
            lecture, data=update_data, partial=True
        )
        if not update_serializer.is_valid():
            raise ValidationError(update_serializer.errors)
        lecture = update_serializer.save()

        return {
            "message": "Lecture updated successfully",
            "status_code": status.HTTP_200_OK,
            "data": update_serializer.data,
        }

    @classmethod
    def delete_lecture(cls, lecture_id):
        lecture = get_lecture_from_id(lecture_id)
        lecture.delete()

        return {
            "message": "Lecture deleted successfully",
            "status_code": status.HTTP_204_NO_CONTENT,
        }
