from django.db.models.signals import post_save
from django.dispatch import receiver
from community.model.models import Comment, Alarm


def create_alarm_on_comment(sender, instance, created, **kwargs):
    if created:
        Alarm.objects.create(receive_user=instance.post.author, comment=instance)


post_save.connect(create_alarm_on_comment, sender=Comment)
