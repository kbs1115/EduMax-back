from django.urls import path

from community.view.post_view import PostView, GetPostsView

app_name = "community"

urlpatterns = [
    path('post/', PostView.as_view(), name="post"),
    path('post/<int:post_id>', PostView.as_view(), name="post"),
    path('posts/', GetPostsView.as_view(), name="posts")
]
