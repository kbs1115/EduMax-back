from django.contrib.sites import requests
from firebase_admin import messaging
from abc import ABC, abstractmethod

from firebase_admin._messaging_utils import UnregisteredError


class NotificationException(Exception):
    pass


class InvalidToken(NotificationException):
    pass


class UnregisterBrowser(NotificationException):
    pass


class NotificationServiceFactory:
    @staticmethod
    def get_service(service_type):
        if service_type == "FCM":
            return FcmNotificationService()
        raise ValueError("Unsupported service type")


class NotificationParams:
    def __init__(self, token, title, body, extra_params=None):
        self.token = token
        self.title = title
        self.body = body
        self.extra_params = extra_params or {}


class NotificationServiceInterface(ABC):
    @abstractmethod
    def send_notification(self, params: NotificationParams):
        """
        interface
        """
        pass


class FcmNotificationService(NotificationServiceInterface):
    def send_notification(self, params: NotificationParams):
        if not self.check_fcm_token(params.token):
            raise InvalidToken
        message = messaging.Message(
            notification=messaging.Notification(
                title=params.title,
                body=params.body
            ),
            token=params.token
        )

        try:
            response = messaging.send(message)
            print('Successfully sent message:', response)
        except UnregisteredError:
            raise UnregisterBrowser

    @classmethod
    def check_fcm_token(cls, token):
        # 메시지 객체 생성
        message = messaging.Message(token=token)

        # 메시지 전송 시도
        try:
            response = messaging.send(message, dry_run=True)  # token 유효성만 판단
            print('this is valid fcm_token:', response)
            return True

        except Exception as e:
            print('invalid token:', e)
            return False
