from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated, IsAdminUser
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.response import Response

from community.model.access import check_lecture_inst_exist_with_playlist_id
from community.view.validation import (
    validate_query_params,
    LectureQueryParam,
    validate_path_params,
    validate_body_request,
    CreateLectureRequestBody,
    LecturePathParam,
    UpdateLectureRequestBody,
)
from community.service.lecture_service import LecturesService, LectureService


class staffOnlyWrite(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj_id):
        if request.user:
            if obj_id == request.user.id:
                return True
            raise PermissionDenied("You can only modify your lecture")
        raise NotAuthenticated()


class GetLecturesView(APIView):
    parser_classes = [JSONParser]
    permission_classes = [staffOnlyWrite]

    @validate_query_params(LectureQueryParam)
    def get(self, request, validated_query_params):
        params = {
            "page": validated_query_params.page,
            "category": validated_query_params.category,
            "search_filter": validated_query_params.search_filter,
            "kw": validated_query_params.q,
        }
        response = LecturesService.get_lectures(**params)

        return Response(
            status=response.get("status_code"),
            data={
                "message": response.get("message", None),
                "data": response.get("data", None),
            },
        )


class LectureView(APIView):
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated | staffOnlyWrite]

    @validate_path_params(LecturePathParam)
    def get(self, request, lecture_id):
        # retrieve
        response = LectureService.get_lecture(lecture_id)
        return Response(
            status=response.get("status_code"),
            data={
                "message": response.get("message", None),
                "data": response.get("data", None),
            },
        )

    @validate_body_request(CreateLectureRequestBody)
    def post(self, request, validated_request_body):
        body = {
            "category_d1": validated_request_body.category_d1,
            "category_d2": validated_request_body.category_d2,
            "category_d3": validated_request_body.category_d3,
            "category_d4": validated_request_body.category_d4,
            "title": validated_request_body.title,
            "youtube_id": validated_request_body.youtube_id,
            "author": request.user,
        }

        response = LectureService.create_lecture(**body)
        return Response(
            status=response.get("status_code"),
            data={
                "message": response.get("message", None),
                "data": response.get("data", None),
            },
        )

    @validate_body_request(UpdateLectureRequestBody)
    @validate_path_params(LecturePathParam)
    def patch(self, request, lecture_id, validated_request_body):
        lecture_author_id = LectureService.get_lecture_user_id(lecture_id)
        self.check_object_permissions(request, lecture_author_id)

        body = {
            "category_d1": validated_request_body.category_d1,
            "category_d2": validated_request_body.category_d2,
            "category_d3": validated_request_body.category_d3,
            "category_d4": validated_request_body.category_d4,
            "title": validated_request_body.title,
            "youtube_id": validated_request_body.youtube_id,
        }
        response = LectureService.update_lecture(lecture_id, **body)
        return Response(
            status=response.get("status_code"),
            data={
                "message": response.get("message", None),
                "data": response.get("data", None),
            },
        )

    @validate_path_params(LecturePathParam)
    def delete(self, request, lecture_id):
        lecture_author_id = LectureService.get_lecture_user_id(lecture_id)
        self.check_object_permissions(request, lecture_author_id)

        response = LectureService.delete_lecture(lecture_id)
        return Response(
            status=response.get("status_code"),
            data={"message": response.get("message", None)},
        )


@api_view(["GET"])
@permission_classes([IsAdminUser])
def check_playlist_duplicate(request):
    response = check_lecture_inst_exist_with_playlist_id(request.get['playlist_id'])
    if response is True:
        return Response(status=status.HTTP_200_OK, data={"message": "duplicate"})
    elif response is False:
        return Response(status=status.HTTP_200_OK, data={"message": "no duplicate"})



