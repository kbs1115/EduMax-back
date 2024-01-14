from django.core.exceptions import ValidationError
from django.db import models, IntegrityError
from account.models import User
from community.domain.categories import CategoryDepth1, CategoryDepth2, CategoryDepth3, CategoryDepth4
from community.domain.validation import CategoryValidator, LikeValidator, PostCategories


class Post(models.Model):
    """
    <설명>
    커뮤니티의 게시글이다. 모든 게시글의 종류는 category field로 인해 정해진다.

    <필드>
    category: 게시글의 종류를 나타내는 category field이다.
              community.domain.categories에서 정의하고있다.
    """
    title = models.CharField(max_length=30)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    category = models.CharField(
        max_length=2, choices=PostCategories.choices, default=PostCategories.FREE
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")


class Comment(models.Model):
    """
        <설명>
        게시글의 댓글 model이다.

        <필드>
        parent_comment: 대댓글 기능으로 같은 comment model 클래스의 인스턴스를 외래키로 참조하고있다.
                        depth 는 모델에서 따로 제한하지 않는다.
    """
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey("self", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Alarm(models.Model):
    """
        <설명>
        알람의 유형은 하나이다 -> comment가 달렸을 때 ( 추후 추가될 수도 있음)

        <필드>
        receive_user: 알림을 받을 user를 의미한다.
    """
    receive_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    """
        <설명>
        "좋아요" 리소스는 post 와 comment 둘중 하나의 model을 외래키로 가진다.
         user은 좋아요를 누른 사용자를 의미한다.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, related_name="likes")
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, null=True, blank=True, related_name="likes"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    # valid시 like model의 필드 validator 실행
    def clean(self):
        super().clean()
        LikeValidator.validate(self)


class Lecture(models.Model):
    """
        <설명>
        youtube_id 와 lecture의 category를 저장하고있다.
        category는 계층형 트리구조이며 각 depth 는 category_d1, category_d2 ... 를 의미한다.

        <필드>
        author: edumax 선생님이며 모든 user은 staff이상의 permission을 가지고있다.

    """
    youtube_id = models.CharField(max_length=11)
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

    # db 저장전 category의 validation을 실행
    def save(self, *args, **kwargs):
        CategoryValidator.validate(self)
        super().save(*args, **kwargs)
