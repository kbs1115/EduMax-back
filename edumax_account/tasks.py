from celery import shared_task
from smtplib import SMTPException
from edumax_account.models import EmailTemporaryKey, PwChangeTemporaryQueryParam
from rest_framework import exceptions
from django.core.mail import EmailMessage

@shared_task(name="delete_email_key_instance")
def delete_email_key_instance(inst_id):
    try:
        email_key_instance = EmailTemporaryKey.objects.get(id=inst_id)
        email_key_instance.delete()
    except EmailTemporaryKey.DoesNotExist:
        raise exceptions.APIException("왜없음?")


@shared_task(name="delete_query_param_instance")
def delete_query_param_instance(inst_id):
    try:
        email_key_instance = PwChangeTemporaryQueryParam.objects.get(id=inst_id)
        email_key_instance.delete()
    except EmailTemporaryKey.DoesNotExist:
        raise exceptions.APIException("왜없음?")

@shared_task(name="async_send_email")
def async_send_email(email_data):
    """
    비동기 이메일 전송 Celery Task
    """
    try:
        # JSON 데이터를 다시 EmailMessage 객체로 변환
        email_message = EmailMessage(
            subject=email_data["subject"],
            body=email_data["body"],
            from_email=email_data["from_email"],
            to=email_data["to"],
        )
        email_message.content_subtype = 'html'  # HTML 이메일 설정
        email_message.send()
    except SMTPException as e:
        raise exceptions.APIException(str(e))
        