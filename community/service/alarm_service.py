import status as status
from django.core.paginator import Paginator
from community.model.alarm_access import get_alarm_from_user
from community.serializers import AlarmRetrieveSerializer
from community.domain.definition import ALARM_LIST_PAGE_SIZE
from rest_framework import status


class AlarmListService:
    def get_alarms(self, user_id, page) -> dict[str, any]:
        alarms = get_alarm_from_user(user_id)

        pagination = Paginator(alarms, ALARM_LIST_PAGE_SIZE)
        page_obj = pagination.page(page).object_list
        list_size = len(page_obj)

        serializer = AlarmRetrieveSerializer(page_obj, many=True)
        return {
            "status": status.HTTP_200_OK,
            "message": "alarms list successfully",
            "data": {
                "page": page,  # 현재 페이지
                "page_size": ALARM_LIST_PAGE_SIZE,  # 한페이지당 게시글 개수
                "total_page_count": alarms.count() // ALARM_LIST_PAGE_SIZE + 1,
                "list_size": list_size,  # 게시글 개수
                "alarm_list": serializer.data,
            }
        }


alarm_list_service = AlarmListService()
