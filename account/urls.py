from django.urls import path, include
from .views import AuthAPIView, SignUpAPIView, TestViewSet
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import routers

router = routers.DefaultRouter()
router.register("test", TestViewSet)

urlpatterns = [
    path("signup/", SignUpAPIView.as_view(), name="signup"),
    path("token/", AuthAPIView.as_view(), name="token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="tokenRefresh"),
    path("", include(router.urls)),
]
