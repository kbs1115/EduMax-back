from celery import shared_task

from account.models import EmailTemporaryKey
from rest_framework import exceptions


@shared_task(name="send_email")
def delete_email_key_instance(inst_id):
    try:
        email_key_instance = EmailTemporaryKey.objects.get(id=inst_id)
        email_key_instance.delete()
    except EmailTemporaryKey.DoesNotExist:
        raise exceptions.APIException("왜없음?")

