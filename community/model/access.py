from rest_framework.exceptions import NotFound
from community.model.models import Post, Comment


def get_post_from_id(id):
    try:
        instance = Post.objects.get(pk=id)
        return instance
    except Post.DoesNotExist:
        raise NotFound("Post does not exists")


def get_parent_post_id(comment_id):
    try:
        comment = Comment.objects.get(pk=comment_id)
        return comment.post.id
    except Comment.DoesNotExist:
        raise NotFound("Parent Comment does not exists")


def get_comment_user_id(comment_id):
    try:
        comment = Comment.objects.get(pk=comment_id)
        return comment.author.id
    except Comment.DoesNotExist:
        raise NotFound("Comment not found")


def get_comment_from_id(comment_id):
    try:
        comment = Comment.objects.get(pk=comment_id)
        return comment
    except Comment.DoesNotExist:
        raise NotFound("comment not found")
