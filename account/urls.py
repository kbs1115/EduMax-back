from django.urls import path
from .views import AuthAPIView, SignUpAPIView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("signup/", SignUpAPIView.as_view()),
    path("token/", AuthAPIView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
]
