from django.db import transaction
from rest_framework import exceptions
from allauth.socialaccount.models import SocialAccount

from edumax_account.models import User
from edumax_account.models import PwChangeTemporaryQueryParam


def get_user_with_email(email):
    """
    이메일로 유저인스턴스를 가져온다.
    """
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        raise exceptions.NotFound("user not found")


def get_social_user_with_user(user):
    """
    Social user instance를 원래 User instance로부터 가져온다.
    """
    try:
        return SocialAccount.objects.get(user=user)
    except SocialAccount.DoesNotExist:
        raise exceptions.NotFound("Social account not found")


def get_number_of_social_account(provider):
    return len(SocialAccount.objects.filter(provider=provider))


def set_password(user, pw):
    with transaction.atomic():
        user.set_password(pw)
        user.save()


def check_user_exists_with_field(field, value):
    """
    유저인스턴스가 있는지 확인한다.
    """
    if field == User.EMAIL_FIELD:
        return User.objects.filter(email=value).exists()
    elif field == User.NICKNAME_FIELD:
        return User.objects.filter(nickname=value).exists()
    elif field == User.USERNAME_FIELD:
        return User.objects.filter(login_id=value).exists()


def get_user_with_pk(pk):
    try:
        return User.objects.get(id=pk)
    except User.DoesNotExist:
        raise exceptions.NotFound("user not found")


def delete_user_db(user):
    user.delete()


def check_pw_change_page_query_param(verify):
    try:
        PwChangeTemporaryQueryParam.objects.get(query_param=verify)
    except PwChangeTemporaryQueryParam.DoesNotExist:
        raise exceptions.ValidationError("wrong query param")
