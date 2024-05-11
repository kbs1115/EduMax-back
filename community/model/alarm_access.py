from django.db.models import Q, Count
from rest_framework import exceptions

from community.model.models import Alarm

def get_alarm_from_user(user_id):
    alarms = Alarm.objects.filter(receive_user=user_id).order_by('-created_at')
    return alarms