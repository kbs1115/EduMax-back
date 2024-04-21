from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from community.model.post_access import get_post_user_id
from community.view.validation import validate_query_params, \
    PostQueryParam, PostPathParam, validate_path_params, validate_body_request, CreatePostRequestBody, \
    UpdatePostRequestBody
from community.service.post_service import PostService, PostsService
from community.service.alarm_service import alarm_list_service


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj_id):
        if request.user:
            if obj_id == request.user.id:
                return True
            raise PermissionDenied()
        raise NotAuthenticated()
    

class AlarmListView(APIView):
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    permission_classes = [IsAuthenticated | IsOwner]
    
    def get(self, request):
        res = alarm_list_service.get_alarms(request.user.id)
        
        response = Response(
            status=res.get("status_code"),
            data = {
                "message": res.get("message", None),
                "data": res.get("data", None)},
        )
        return response
    
    
    