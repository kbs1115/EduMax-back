from rest_framework import serializers

from account.models import User
from .models import Post, Comment, File


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "nickname"]


class FileSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), allow_null=True, required=False)
    comment = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), allow_null=True, required=False)

    class Meta:
        model = File
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    files = FileSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = ['title', 'html_content', 'created_at', 'modified_at', 'category', 'category',
                  'author', 'content', 'files']


class PostListSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Post
        fields = ['title', 'html_content', 'created_at', 'modified_at', 'category', 'category',
                  'author']
