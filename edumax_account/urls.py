from django.urls import path, include
from edumax_account.view.email_views import EmailSenderApiView
from edumax_account.view.user_views import *
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import routers
from edumax_account.view.user_views import DuplicateCheckerAPIView
from edumax_account.view.social_login_views import (
    google_oauth_redirect,
    google_callback,
)

app_name = "edumax_account"

urlpatterns = [
    path("email-send/", EmailSenderApiView.as_view()),  # 이메일 보내기
    path("user/", UserAPIView.as_view(), name="user"),
    path(
        "user/<int:pk>/", CertainUserAPIView.as_view(), name="certainUser"
    ),  # user auth
    path(
        "user/duplicate-check/", DuplicateCheckerAPIView.as_view()
    ),  # 회원가입만을 위한 중복체커여서 확장성 떨어져보여서 맘에안듦
    path(
        "user/id-find/email-auth/", GetLoginIdApiView.as_view()
    ),  # id 찾기위한 이메일 인증
    path(
        "user/pw-change/email-auth/", RedirectPwChangeApiView.as_view()
    ),  # pw 변경하기위한 이메일 인증
    path("user/pw-change/", PasswordChangeApiView.as_view()),  # pw 변경 페이지
    path("token/", AuthAPIView.as_view(), name="token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="tokenRefresh"),
    # 구글 소셜로그인
    path("user/google/login/", google_oauth_redirect, name="google_login"),
    path("user/google/redirection/", google_callback, name="google_callback"),
]
