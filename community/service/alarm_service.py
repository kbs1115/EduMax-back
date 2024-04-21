import status as status
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator, EmptyPage
from django.db import transaction
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser

from community.model.alarm_access import get_alarm_from_user
from community.serializers import AlarmRetrieveSerializer
from community.domain.definition import POST_LIST_PAGE_SIZE, PostFilesState
from rest_framework import status, exceptions

from community.service.file_service import FileService
from community.service.permission import only_staff_can_create_post_notice

class AlarmListService:
    def get_alarms(self, user_id):
        alarm = get_alarm_from_user(user_id, 20, 1)
        
        serializer = AlarmRetrieveSerializer(alarm, many=True)
        return {
            "status": status.HTTP_200_OK,
            "message": "alarm retrieve successfully",
            "data": serializer.data,
        }
            
    
alarm_list_service = AlarmListService()