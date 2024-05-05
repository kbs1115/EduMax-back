from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from edumax_account.model.user_access import save_user_fcm_token
from edumax_account.utils.notification_utils import FcmNotificationService


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def save_web_push_token(request):
    user = request.user
    fcm_token = request.data.get('token')

    # token valid 확인
    if FcmNotificationService.check_fcm_token(fcm_token):
        save_user_fcm_token(user=user, valid_fcm_token=fcm_token)
        return Response(status=status.HTTP_200_OK,
                        data={
                            "message": "error : token received successfully."
                        }
                        )
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={
                            "message": "error : there is no fcm token."
                        }
                        )

