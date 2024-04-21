from django.db.models import Q, Count
from django.core.paginator import Paginator
from rest_framework import exceptions

from community.model.models import Alarm

def get_alarm_from_user(user_id, page_size, page):
    alarms = Alarm.objects.filter(receive_user=user_id)
    if not alarms.exists():
        raise exceptions.NotFound("Alarm not found")
    
    paginator = Paginator(alarms, page_size)
    # 일반적으로 페이지 번호는 요청에서 받거나 기본값으로 설정합니다.
    # 여기서는 예시로 1페이지를 사용합니다.
    page_number = page
    page_obj = paginator.get_page(page_number)
    
    return page_obj