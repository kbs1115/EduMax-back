import random
from datetime import datetime, timezone, timedelta
from django.db import transaction
from django.template.loader import render_to_string
from rest_framework import exceptions, status

from edumax_account.model.temp_access import (
    create_email_key_model_instance,
    validate_email_key,
)
from edumax_account.tasks import delete_email_key_instance, async_send_email
from config.settings.base import EMAIL_HOST_USER


class EmailService:
    @classmethod
    def generate_random_number(cls):
        return "".join(random.choice("0123456789") for _ in range(6))

    """
    추가로 고려해줘야할점:
    1. 이메일 전송 제한을 걸어야함.(기준은 ip, 혹은 토큰이 될거같음)->service 단 validator
    """

    def send_email(self, email):
        """
        이메일을 받아서 임시키를 만든 후 DB에 저장하고
        이메일로 임시키를 전송한다.
        해당 임시키는 DB에 5분 동안 유지되며 자동으로 삭제된다.
        """

        subject = "EduMax 이메일 인증"  # 타이틀
        to = [email]  # 수신할 이메일 주소
        from_email = EMAIL_HOST_USER  # 발신할 이메일 주소
        auth_key = self.generate_random_number()

        context = {'verification_code': auth_key}
        html_content = render_to_string('email_template.html', context)

        
        with transaction.atomic():
            # DB에 인증 키 저장
            inst = create_email_key_model_instance(email, auth_key)
            # Celery Worker에 전달할 수 있도록 데이터 직렬화 (JSON 변환)
            email_data = {
                "subject": subject,
                "body": html_content,
                "from_email": from_email,
                "to": to
            }
            # Worker에게 실행 (비동기 이메일 전송)
            async_send_email.apply_async(args=[email_data])
            # 5분 후 이메일 키 삭제
            eta = datetime.now(timezone.utc) + timedelta(minutes=5)
            delete_email_key_instance.apply_async(
                    (inst.id,), eta=eta
                )  # 5분후에 worker에게 삭제 명령
            return {
                "message": "email sent successfully",
                "status_code": status.HTTP_200_OK,
            }
            
    
    """
        추가로 고려해줘야할점:
        1. 횟수제한 걸어야함.(3번이상 틀리면 ip차단시킨다던가) ->service 단 validator
    """

    def check_authentication(self, email, auth_key):
        """
        auth_key와 db의 키를 비교하고 다를경우 raise
        """
        if validate_email_key(email=email, auth_key=auth_key):
            return {
                "message": "email authenticated successfully",
                "status_code": status.HTTP_200_OK,
            }
