from django.urls import path

from community.view.post_view import PostView, GetPostsView
from community.view.comment_view import MakeCommentToPostView, CommentView
from community.view.lecture_view import LectureView, GetLecturesView

app_name = "community"

urlpatterns = [
    path("post/", PostView.as_view()),
    path("post/<int:post_id>", PostView.as_view()),
    path("posts/", GetPostsView.as_view(), name="posts"),
    path(
        "post/<int:post_id>/comment/",
        MakeCommentToPostView.as_view(),
        name="post_comment",
    ),
    path("comment/<int:comment_id>", CommentView.as_view(), name="comment"),
    path("lectures/", GetLecturesView.as_view(), name="lectures"),
    path("lecture/", LectureView.as_view(), name="lectures"),
    path("lecture/<int:lecture_id>", LectureView.as_view(), name="lecture"),
]
