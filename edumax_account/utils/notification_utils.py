from django.contrib.sites import requests
from firebase_admin import messaging
from abc import ABC, abstractmethod

from rest_framework.exceptions import ValidationError


class NotificationServiceInterface(ABC):
    @abstractmethod
    def send_notification(self, **kwargs):
        """
        interface
        """
        pass


class FcmNotificationService(NotificationServiceInterface):
    def send_notification(self, **kwargs):
        token = kwargs.get('token')
        title = kwargs.get('title')
        body = kwargs.get('body')

        if self.check_fcm_token(token) is not True:
            raise ValidationError
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=token,
        )
        try:
            response = messaging.send(message)
            print('Successfully sent message:', response)
        except Exception:
            print("FCM Token is invalid or has expired.")
            raise ValidationError

    @classmethod
    def check_fcm_token(cls, token):
        # 메시지 객체 생성
        message = messaging.Message(token=token)

        # 메시지 전송 시도
        try:
            response = messaging.send(message, dry_run=True)  # token 유효성만 판단
            print('Successfully sent message:', response)
            return True

        except Exception as e:
            print('invalid token:', e)
            return False


def notification_service(service, **kwargs):
    service.send_notification(**kwargs)
