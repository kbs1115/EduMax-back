from django.urls import path

from community.view.post_view import PostView, GetPostsView

urlpatterns = [
    path('post/', PostView.as_view()),
    path('post/<int:post_id>', PostView.as_view()),
    path('posts/', GetPostsView.as_view())
]
