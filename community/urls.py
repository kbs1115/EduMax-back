from django.urls import path

from community.view.s3_file_view import s3_uploader
from community.view.like_view import LikeToPostView, LikeToCommentView
from community.view.post_view import PostView, GetPostsView
from community.view.comment_view import MakeCommentToPostView, CommentView
from community.view.lecture_view import LectureView, GetLecturesView

app_name = "community"

urlpatterns = [
    path("post/", PostView.as_view(), name="post"),
    path("post/<int:post_id>", PostView.as_view(), name="post"),
    path("post/<int:post_id>/like", LikeToPostView.as_view(), name="post_like"),
    path("posts/", GetPostsView.as_view(), name="posts"),
    path(
        "post/<int:post_id>/comment/",
        MakeCommentToPostView.as_view(),
        name="post_comment",
    ),
    path("comment/<int:comment_id>", CommentView.as_view(), name="comment"),
    path("comment/<int:comment_id>/like", LikeToCommentView.as_view(), name="comment_like"),

    path("lectures/", GetLecturesView.as_view(), name="lectures"),
    path("lecture/", LectureView.as_view(), name="lectures"),
    path("lecture/<int:lecture_id>", LectureView.as_view(), name="lecture"),
    path("s3_files/", s3_uploader)
]
