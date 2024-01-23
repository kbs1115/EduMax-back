from rest_framework import serializers

from account.models import User
from .models import Post, Comment, File


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "nickname"]


class FileSerializer(serializers.ModelSerializer):
    # post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), allow_null=True, required=False)
    # comment = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), allow_null=True, required=False)

    class Meta:
        model = File
        fields = "__all__"


class PostRetrieveSerializer(serializers.ModelSerializer):
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
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Post
        fields = ['title', 'html_content', 'created_at', 'modified_at', 'category',
                  'author']


class PostListSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        queryset=File.objects.all(),
        slug_field='nickname'
    )

    class Meta:
        model = Post
        fields = ['title', 'html_content', 'created_at', 'modified_at', 'category', 'content',
                  'author']
