import random
from datetime import datetime, timezone, timedelta
from smtplib import SMTPException

from django.core.mail import EmailMessage
from django.db import transaction
from rest_framework import exceptions, status

from account.model.temp_access import create_email_key_model_instance, validate_email_key
from account.tasks import delete_email_key_instance
from config.settings import EMAIL_HOST_USER


class EmailService:
    @classmethod
    def generate_random_number(cls):
        return ''.join(random.choice('0123456789') for _ in range(6))

    """
    추가로 고려해줘야할점:
    1. 이메일 전송 제한을 걸어야함.(기준은 ip, 혹은 토큰이 될거같음)->service 단 validator
    """

    def send_email(self, email):
        """
        이메일을 받아서 임시키를 만든후 db에 저장하고
        이메일로 임시키를 전송한다.
        해당 임시키는 db에 5분동안 유지되며 자동으로 삭제된다.
        """

        subject = "EduMax 이메일 인증"  # 타이틀
        to = [email]  # 수신할 이메일 주소
        from_email = EMAIL_HOST_USER  # 발신할 이메일 주소
        auth_key = self.generate_random_number()
        message = f"인증번호: \n{auth_key}"  # 본문 내용

        try:
            with transaction.atomic():
                inst = create_email_key_model_instance(email, auth_key)
                EmailMessage(
                    subject=subject,
                    body=message,
                    to=to,
                    from_email=from_email
                ).send()  # 만약 없는 메일이라고 하면 아무런 응답이 없음 에러도 안뜸

                eta = datetime.now(timezone.utc) + timedelta(minutes=5)
                delete_email_key_instance.apply_async((inst.id,), eta=eta)  # 5분후에 worker에게 삭제 명령

                return {"message": "email sent successfully", "status_code": status.HTTP_200_OK}
        except SMTPException as e:
            raise exceptions.APIException(str(e))

    """
        추가로 고려해줘야할점:
        1. 횟수제한 걸어야함.(3번이상 틀리면 ip차단시킨다던가) ->service 단 validator
    """

    def check_authentication(self, email, auth_key):
        """
        auth_key와 db의 키를 비교하고 다를경우 raise
        """
        if validate_email_key(email=email, auth_key=auth_key):
            return {"message": "email authenticated successfully", "status_code": status.HTTP_200_OK}
