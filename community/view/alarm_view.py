from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from community.model.post_access import get_post_user_id
from community.view.validation import validate_query_params, AlarmQueryParam
from community.service.post_service import PostService, PostsService
from community.service.alarm_service import alarm_list_service


class AlarmListView(APIView):
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    permission_classes = [IsAuthenticated]

    # user_id랑 해당 user의 alarm을 가져오는거
    @validate_query_params(AlarmQueryParam)
    def get(self, request, validated_query_params):
        response = alarm_list_service.get_alarms(request.user.id, validated_query_params.page)

        return Response(status=response.get("status_code"),
                        data={
                            "message": response.get("message", None),
                            "data": response.get("data", None)},
                        )
