from rest_framework import serializers

from account.models import User
from .models import Post, Comment, File


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
        queryset=User.objects.all(),
        slug_field='nickname'
    )
    # 해당 post_id 와 관련된 files
    files = FileSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['title', 'html_content', 'created_at', 'modified_at', 'category',
                  'author', 'files']


class PostCreateSerializer(serializers.ModelSerializer):
    """
        - post model에 들어가는 input 시리얼라이저
    """
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Post
        fields = ['title', 'html_content', 'created_at', 'modified_at', 'category',
                  'author']


class PostListSerializer(serializers.ModelSerializer):
    """
        - PostList 를 위한 output 시리얼라이저
        - author의 닉네임을 보내줌
    """
    author = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='nickname'
    )

    class Meta:
        model = Post
        fields = ['title', 'html_content', 'created_at', 'modified_at', 'category', 'content',
                  'author']
