from rest_framework import serializers


from edumax_account.models import User
from .model.models import Post, Comment, File, Lecture, Like, Alarm
from community.domain.validation import CategoryValidator


class LikeCreateSerializer(serializers.ModelSerializer):
    """
    like 생성을 위한 serializer
    """

    class Meta:
        model = Like
        fields = "__all__"


class LikeRetrieveSerializer(serializers.ModelSerializer):
    """
    좋아요리소스에 대한 output serializer
    """
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field="nickname"
    )

    class Meta:
        model = Like
        fields = [
            "post",
            "comment",
            "user"
        ]


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
    # 해당 post_id 와 관련된 likes
    likes = LikeRetrieveSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "html_content",
            "created_at",
            "modified_at",
            "category",
            "author",
            "files",
            "likes",
            "views"
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
    likes_count = serializers.SerializerMethodField(method_name="get_likes_count")
    comments_count = serializers.SerializerMethodField(method_name="get_comments_count")

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "html_content",
            "created_at",
            "modified_at",
            "category",
            "content",
            "author",
            "likes_count",
            "comments_count",
            "views"
        ]

    def get_likes_count(self, obj):
        # obj는 Post 모델의 인스턴스
        return obj.likes.count()
    
    def get_comments_count(self, obj):
        # obj는 Post 모델의 인스턴스
        return obj.comments.count()


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
    post_id = serializers.PrimaryKeyRelatedField(read_only=True)

    # 해당 post_id 와 관련된 files
    files = FileSerializer(many=True, read_only=True)

    # 해당 post_id 와 관련된 likes
    likes = LikeRetrieveSerializer(many=True, read_only=True)
    
    likes_count = serializers.SerializerMethodField(method_name="get_likes_count")
    post_title = serializers.SerializerMethodField(method_name="get_post_title")

    class Meta:
        model = Comment
        fields = [
            "id",
            "content",
            "html_content",
            "created_at",
            "modified_at",
            "author",
            "files",
            "likes",
            "likes_count",
            "post_id",
            "post_title"
        ]
        
    def get_likes_count(self, obj):
        # obj는 Post 모델의 인스턴스
        return obj.likes.count()
    
    def get_post_title(self, obj):
        # obj는 Comment 모델의 인스턴스
        return obj.post.title


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
            "id",
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


class AlarmRetrieveSerializer(serializers.ModelSerializer):
    comment_author = serializers.SerializerMethodField()
    post_id = serializers.SerializerMethodField()
    post_title = serializers.SerializerMethodField()
    receive_user = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field='nickname'
    )

    class Meta:
        model = Alarm
        fields = [
            'id',
            'receive_user',
            'comment_author',
            'post_id',
            'post_title',
            'created_at'
        ]
        
    def get_comment_author(self, obj):
        return obj.comment.author.nickname if obj.comment and obj.comment.author else None

    def get_post_id(self, obj):
        return obj.comment.post.id if obj.comment and obj.comment.post else None

    def get_post_title(self, obj):
        return obj.comment.post.title if obj.comment and obj.comment.post else None