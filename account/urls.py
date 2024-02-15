from django.urls import path, include
from .view.user_views import *
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import routers
from account.view.user_views import DuplicateCheckerAPIView

app_name = "account"

router = routers.DefaultRouter()
router.register("test", TestViewSet)

urlpatterns = [
    path(
        "user/check-duplicate/", DuplicateCheckerAPIView.as_view()
    ),  # 회원가입만을 위한 중복체커여서 확장성 떨어져보여서 맘에안듦
    path("user/send-email/", EmailSenderApiView.as_view()),  # 이메일 보내기
    path(
        "user/email-authenticate/", EmailAuthenticationApiView.as_view()
    ),  # 이메일 인증
    path("user/<int:pk>/", CertainUserAPIView.as_view(), name="certainUser"),
    path("user/", UserAPIView.as_view(), name="user"),
    path("token/", AuthAPIView.as_view(), name="token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="tokenRefresh"),
    path("", include(router.urls)),
]
