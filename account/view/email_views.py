from django.http import JsonResponse
from rest_framework.views import APIView

from account.service.email_service import EmailService
from account.validators import EmailFieldModel
from community.view.validation import validate_body_request


class EmailSenderApiView(APIView):
    """
    이메일을 받아서 인증키를 생성후 db 저장한다.
    생성한 인증키를 이메일로 보낸다.
    """
    @validate_body_request(EmailFieldModel)
    def post(self, request, validated_request_body):
        email = {'email': validated_request_body.email}
        response = EmailService().send_email(**email)
        return JsonResponse(status=response.get("status_code"),
                            data={
                                "message": response.get("message", None),
                                "data": response.get("data", None)},
                            )
