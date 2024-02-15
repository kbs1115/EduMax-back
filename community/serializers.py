from rest_framework import serializers

from account.models import User
from .model.models import Post, Comment, File, Lecture
from community.domain.validation import CategoryValidator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "nickname"]


class FileSerializer(serializers.ModelSerializer):
    """
    - file model에 들어가는 input 시리얼라이저
    """

    class Meta:
        model = File
        fields = "__all__"


class PostRetrieveSerializer(serializers.ModelSerializer):
    """
    - PostRetrieve 를 위한 output 시리얼라이저
    - 해당 post_id를 외래키로 가지고있는 files도 같이 보내줌.
    - author의 닉네임을 보내줌
    """

    author = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field="nickname"
    )
    # 해당 post_id 와 관련된 files
    files = FileSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "title",
            "html_content",
            "created_at",
            "modified_at",
            "category",
            "author",
            "files",
        ]


class PostCreateSerializer(serializers.ModelSerializer):
    """
    - post model에 들어가는 input 시리얼라이저
    """

    class Meta:
        model = Post
        fields = "__all__"


class PostListSerializer(serializers.ModelSerializer):
    """
    - PostList 를 위한 output 시리얼라이저
    - author의 닉네임을 보내줌
    """

    author = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field="nickname"
    )

    class Meta:
        model = Post
        fields = [
            "title",
            "html_content",
            "created_at",
            "modified_at",
            "category",
            "content",
            "author",
        ]


class CommentCreateSerializer(serializers.ModelSerializer):
    """
    - comment model에 들어가는 input 시리얼라이저
    """

    class Meta:
        model = Comment
        fields = "__all__"


class CommentRetrieveSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field="nickname"
    )

    # 해당 post_id 와 관련된 files
    files = FileSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = [
            "content",
            "html_content",
            "created_at",
            "modified_at",
            "author",
            "files",
        ]


class LectureListSerializer(serializers.ModelSerializer):
    """
    - LectureList 를 위한 output 시리얼라이저
    - author의 닉네임을 보내줌
    """

    author = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field="nickname"
    )

    class Meta:
        model = Lecture
        fields = [
            "title",
            "youtube_id",
            "created_at",
            "modified_at",
            "author",
        ]


class LectureRetrieveSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field="nickname"
    )

    class Meta:
        model = Lecture
        fields = [
            "title",
            "youtube_id",
            "category_d1",
            "category_d2",
            "category_d3",
            "category_d4",
            "created_at",
            "modified_at",
            "author",
        ]


class LectureCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lecture
        fields = "__all__"

    def validate(self, data):
        CategoryValidator.validate(data)
        return data
