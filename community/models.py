from django.db import models, IntegrityError
from account.models import User


class Post(models.Model):
    class Categories(models.TextChoices):
        FREE = "FR"
        NOTICE = "NO"
        KOREAN_QUESTION = "KQ"
        ENG_QUESTION = "EQ"
        MATH_QUESTION = "MQ"
        KOREAN_DATA = "KD"
        ENG_DATA = "ED"
        MATH_DATA = "MD"

    title = models.CharField(max_length=30)
    content = models.TextField()
    created_at = models.DateTimeField()
    category = models.CharField(
        max_length=2, choices=Categories.choices, default=Categories.FREE
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey("self", on_delete=models.CASCADE)
    created_at = models.DateTimeField()


class Alarm(models.Model):
    receive_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    created_at = models.DateTimeField()


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, null=True, blank=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        # 객체 저장 전에 post나 comment 둘 중 하나만 값이 있는지 체크
        if not (self.post is None) ^ (self.comment is None):
            raise IntegrityError("post나 comment 중 하나에만 like를 추가할 수 있습니다.")
        super().save(*args, **kwargs)


class Lecture(models.Model):
    youtube_id = models.CharField(max_length=20)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Category_depth1(models.TextChoices):
        KOREAN = "KO"
        ENGLISH = "EN"
        MATH = "MA"

    class Category_depth2(models.TextChoices):
        SCHOOL_TEST = "SC"
        SAT = "SA"
        GRAMMAR = "GR"

    category_d1 = models.CharField(max_length=2, choices=Category_depth1.choices)
    category_d2 = models.CharField(
        max_length=2, choices=Category_depth2.choices, null=True, blank=True
    )
