from django.core.exceptions import ValidationError
from django.db import models, IntegrityError
from account.models import User
from community.domain.lecture_category import CategoryDepth1, CategoryDepth2, CategoryDepth3, CategoryDepth4
from community.domain.validation import CategoryValidator, LikeValidator, PostCategories


class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    # 12.31 수정: create_at 자동화, modify_at field 추가
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    category = models.CharField(
        max_length=2, choices=PostCategories.choices, default=PostCategories.FREE
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")


class Comment(models.Model):
    content = models.TextField()
    # 12.31 수정: related_name 추가
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey("self", on_delete=models.CASCADE)
    # 12.31 수정: create_at 자동화, modify_at field 추가
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Alarm(models.Model):
    receive_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    # 12.31 수정: related_name 추가
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, related_name="likes")
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, null=True, blank=True, related_name="likes"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        super().clean()
        LikeValidator.validate(self)


class Lecture(models.Model):
    # 12.31 수정: 11자로 수정. 유튜브 id 는 최대 문자열 11자임 넘을 경우 validation error
    youtube_id = models.CharField(max_length=11)
    # 12.31 수정: related_name 추가
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lectures")
    category_d1 = models.CharField(max_length=2, choices=CategoryDepth1.choices)
    category_d2 = models.CharField(
        max_length=3, choices=CategoryDepth2.choices, null=True, blank=True
    )
    category_d3 = models.CharField(
        max_length=3, choices=CategoryDepth3.choices, null=True, blank=True
    )
    category_d4 = models.CharField(
        max_length=3, choices=CategoryDepth4.choices, null=True, blank=True
    )

    def save(self, *args, **kwargs):
        CategoryValidator.validate(self)
        super().save(*args, **kwargs)
