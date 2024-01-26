from django.contrib import admin
from django.urls import path

from community.views import PostView, GetPostsView

urlpatterns = [

    path('post/<int:post_id>', PostView.as_view()),
    path('post/', PostView.as_view()),
    path('posts/', GetPostsView.as_view())
]