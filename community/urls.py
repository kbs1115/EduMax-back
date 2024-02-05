from django.urls import path

from community.view.post_view import PostView, GetPostsView
from community.view.comment_view import MakeCommentToPostView, CommentView

app_name = "community"

urlpatterns = [
    path("post/", PostView.as_view()),
    path("post/<int:post_id>", PostView.as_view()),
    path("posts/", GetPostsView.as_view()),
    path(
        "post/<int:post_id>/comment/",
        MakeCommentToPostView.as_view(),
        name="post_comment",
    ),
    path("comment/<int:comment_id>", CommentView.as_view(), name="comment"),
]
