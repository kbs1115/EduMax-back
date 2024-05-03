from django.db.models.signals import post_save
from community.model.models import Comment, Alarm
from edumax_account.model.user_access import delete_user_fcm_token
from edumax_account.utils.notification_utils import FcmNotificationService, \
    NotificationServiceFactory, NotificationParams, InvalidToken, UnregisterBrowser, NotificationException


def handle_alarm_on_comment_create(sender, instance, created, **kwargs):
    if created:
        # alarm instance 생성
        Alarm.objects.create(receive_user=instance.post.author, comment=instance)

        # fcm message 처리
        try:
            post_owner_token = instance.post.author.fcm_token
            if post_owner_token:
                comment_user_nickname = instance.author.nickname  # 댓글 단 유저닉네임
                post_title = instance.post.title  # 댓글이 달린 post title
                post_owner_inst = instance.post.author  # post 게시글 user instance

                # 메세지 생성
                message_title = f"EduMax 알림"
                message_body = f"나의 게시글 '{post_title}'에 {comment_user_nickname} 님의 댓글이 달렸어요."

                params = NotificationParams(token=post_owner_token, title=message_title, body=message_body)
                service = NotificationServiceFactory.get_service('FCM')
                service.send_notification(params)

        except InvalidToken:  # checkToken 과정에서 존재하지않는 token일때
            print("token expired or invalid token")
            delete_user_fcm_token(post_owner_inst)

        except UnregisterBrowser:  # 브라우저의 토큰, 혹은 서비스워커가 삭제되었을때
            print(f"user browser's token deleted or service worker deleted->user_id:{post_owner_inst.id}")
            delete_user_fcm_token(post_owner_inst)
        except NotificationException:
            print("something wrong with connection")


post_save.connect(handle_alarm_on_comment_create, sender=Comment)
