from django.db.models.signals import post_save
from rest_framework.exceptions import ValidationError

from community.model.models import Comment, Alarm
from edumax_account.model.user_access import delete_user_fcm_token
from edumax_account.utils.notification_utils import FcmNotificationService, notification_service


def handle_alarm_on_comment(sender, instance, created, **kwargs):
    if created:
        # alarm instance 생성
        Alarm.objects.create(receive_user=instance.post.author, comment=instance)

        post_owner_token = instance.post.author.fcm_token
        try:
            # fcm message 처리
            if post_owner_token:
                fcm_service = FcmNotificationService()

                comment_user_nickname = instance.author.nickname
                post_title = instance.post.title
                post_owner = instance.post.author

                message_title = f"EduMax 알림"
                message_body = f"나의 게시글 '{post_title}'에 {comment_user_nickname} 님의 댓글이 달렸어요."
                notification_service(
                    fcm_service,
                    token=post_owner_token,
                    title=message_title,
                    body=message_body
                )
        except ValidationError:
            print(f"something wrong with token ->post_id:{post_owner.id}")
            delete_user_fcm_token(post_owner)


post_save.connect(handle_alarm_on_comment, sender=Comment)
