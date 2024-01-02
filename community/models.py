from django.core.exceptions import ValidationError
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
    # 12.31 수정: create_at 자동화, modify_at field 추가
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    category = models.CharField(
        max_length=2, choices=Categories.choices, default=Categories.FREE
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

    # 12.31 수정: 데이터베이스에 저장하기전에 is_valid 검사에서 처리해야할 문제 아닌가 싶음.
    def save(self, *args, **kwargs):
        # 객체 저장 전에 post나 comment 둘 중 하나만 값이 있는지 체크
        if not (self.post is None) ^ (self.comment is None):
            raise IntegrityError("post나 comment 중 하나에만 like를 추가할 수 있습니다.")
        super().save(*args, **kwargs)

    # 12.31 수정: 따라서 저장 단계가 아닌 역직렬화 직후 model field 유효성 검사 단계에서 처리한다.
    # 12.31 수정: 하지만 단점은 is_valid를 수행하지않으면 모름.
    def clean(self):
        super().clean()
        if self.post and self.comment:
            raise ValidationError("post나 comment 중 하나에만 like를 추가할 수 있습니다.")


class Lecture(models.Model):
    # 12.31 수정: 11자로 수정. 유튜브 id 는 최대 문자열 11자임 넘을 경우 validation error
    youtube_id = models.CharField(max_length=11)
    # 12.31 수정: related_name 추가
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lectures")

    # 12.31 수정: camelcase is not used in class name
    class CategoryDepth1(models.TextChoices):

        KOREAN = "KO"
        ENGLISH = "EN"
        MATH = "MA"

    class CategoryDepth2(models.TextChoices):

        # children of ENGLISH
        SCHOOL_TEST = "SC"
        SAT = "SA"
        GRAMMAR = "GR"

    # 12.31 수정: 카테고리 depth 3,4 추가
    class CategoryDepth3(models.TextChoices):

        # children of SCHOOL_TEST
        TEXTBOOK = "TB"
        EBS = "EBS"
        SCHOOL_MOCK_EXAM = "SCM"

        # children of SAT
        SAT_MOCK_EXAM = "SAM"

        # child of GRAMMAR
        POCKET_GRAMMAR = "PGR"
        BASIC_GRAMMAR = "BGR"

    class CategoryDepth4(models.TextChoices):

        # children of TEXTBOOK
        ENGLISH0 = "E0"
        ENGLISH1 = "E1"
        ENGLISH2 = "E2"
        READING_COMPOSITION = "RC"

        # children of SCHOOL_MOCK_EXAM
        HIGH1 = "H1"
        HIGH2 = "H2"

    class _CategoryTree:
        _tree_structure = {
            # english
            "KO": [],
            "En": ["SC", "SA", "GR"],
            "MA": [],

            # eng-depth2
            "SC": ["TB", "EBS", "SCM"],
            "SA": ["SAM"],
            "GR": ["PGR", "BGR"],

            # eng-depth3
            "TB": ["E0", "E1", "E2"],
            "SCM": ["H1", "H2"]
        }

        @classmethod
        def is_valid_category(cls, category, subcategory):
            if category in cls._tree_structure and subcategory in cls._tree_structure[category]:
                return True
            return False

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
        if self.category_d4 and not self.category_d3:
            raise ValidationError('Category Depth 4 requires Category Depth 3')
        if self.category_d3 and not self.category_d2:
            raise ValidationError('Category Depth 3 requires Category Depth 2')
        if self.category_d2 and not self.category_d1:
            raise ValidationError('Category Depth 2 requires Category Depth 1')

        if self.category_d4 and not self._CategoryTree.is_valid_category(self.category_d3, self.category_d4):
            raise ValidationError('category depth 4 cannot exist without category depth 3')
        if self.category_d3 and not self._CategoryTree.is_valid_category(self.category_d2, self.category_d3):
            raise ValidationError('category depth 3 cannot exist without category depth 2')
        if self.category_d2 and not self._CategoryTree.is_valid_category(self.category_d1, self.category_d2):
            raise ValidationError('category depth 2 cannot exist without category depth 1')

        super().save(*args, **kwargs)
