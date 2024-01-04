from django.urls import path, include
from .views import AuthAPIView, SignUpAPIView, TestViewSet
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import routers

router = routers.DefaultRouter()
router.register("test", TestViewSet)

urlpatterns = [
    path("signup/", SignUpAPIView.as_view()),
    path("token/", AuthAPIView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("", include(router.urls)),
]
