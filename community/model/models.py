from django.db import models
from edumax_account.models import User
from community.domain.validation import CategoryValidator, LikeValidator
from community.domain.definition import (
    PostCategories,
    CategoryDepth1,
    CategoryDepth2,
    CategoryDepth3,
    CategoryDepth4,
)


class Post(models.Model):
    """
    <설명>
    커뮤니티의 게시글이다. 모든 게시글의 종류는 category field로 인해 정해진다.
    ckeditor로 부터 받은 html 형식을 html_content에 저장후 해당 게시글을 요청할때 돌려준다.

    <필드>
    category: 게시글의 종류를 나타내는 category field이다.
              community.domain.categories에서 정의하고있다.
    html_content: tag 등이 그대로 남아있는 상태의 content
    content: tag 등이 js redux로 제거된 상태의 content

    <고려사항>
    ckeditor에서 content 뿐만 아니라 title 도 포함할 수 있다.
    -> 해당 아이디어 적용시 html_content 에는 title 도 포함(필드 네임 수정 하는게 좋아 보임)
    """

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30)
    content = models.TextField()
    html_content = models.TextField()
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
    html_content: tag 등이 그대로 남아있는 상태의 content
    content: tag 등이 js redux로 제거된 상태의 content
    """

    id = models.AutoField(primary_key=True)
    content = models.TextField()
    html_content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Alarm(models.Model):
    """
    <설명>
    알람의 유형은 하나이다 -> comment가 달렸을 때 (추후 추가될 수도 있음)

    <필드>
    receive_user: 알림을 받을 user를 의미한다.
    """

    id = models.AutoField(primary_key=True)
    receive_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    """
    <설명>
    "좋아요" 리소스는 post 와 comment 둘중 하나의 model을 외래키로 가진다.
     user은 좋아요를 누른 사용자를 의미한다.
    """

    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, null=True, default=None, related_name="likes"
    )
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, null=True, default=True, related_name="likes"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class File(models.Model):
    """
    <설명>
    현재는 post나 comment에 붙어서 종속적으로 존재한다.
    삭제 시그널 별도로 x
    비지니스 로직상 file을 우선 삭제후 post 혹은 comment 삭제이므로
    delete = CasCade에 의해 삭제된 파일에 추가적인 작업 필요x

    <필드>
    file_location = s3의 파일 리소스 위치이다.
    ->file_service.make_file_path에 의해 만들어진다.
    """

    id = models.AutoField(primary_key=True)
    file_location = models.TextField()
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, null=True, related_name="files", default=None
    )
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, null=True, related_name="files", default=None
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Lecture(models.Model):
    """
    <설명>
    youtube_id 와 lecture의 category를 저장하고있다.
    category는 계층형 트리구조이며 각 depth 는 category_d1, category_d2 ... 를 의미한다.

    <필드>
    author: edumax 선생님이며 모든 user은 staff이상의 permission을 가지고있다.

    """

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30)
    youtube_id = models.CharField(unique=True, max_length=11)
    # edumax 가입 user model 을 author 로 써야할지 말아야할지 고민중
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lectures")
    category_d1 = models.CharField(max_length=2, choices=CategoryDepth1.choices)
    category_d2 = models.CharField(
        max_length=3, choices=CategoryDepth2.choices, null=True, default=None
    )
    category_d3 = models.CharField(
        max_length=3, choices=CategoryDepth3.choices, null=True, default=None
    )
    category_d4 = models.CharField(
        max_length=3, choices=CategoryDepth4.choices, null=True, default=None
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


