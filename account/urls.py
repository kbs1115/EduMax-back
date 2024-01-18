from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import routers


app_name = "account"

router = routers.DefaultRouter()
router.register("test", TestViewSet)


urlpatterns = [
    path("user/", UserAPIView.as_view(), name="user"),
    path("user/<int:pk>/", CertainUserAPIView.as_view(), name="certainUser"),
    path("token/", AuthAPIView.as_view(), name="token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="tokenRefresh"),
    path("", include(router.urls)),
]
