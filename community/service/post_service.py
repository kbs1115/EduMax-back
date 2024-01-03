from community.models import Post
from community.serializers import PostSerializer


class PostService:

    def get_posts(self, title):
        posts = Post.objects.filter(title=title)
        serializer = PostSerializer(posts)
        return serializer.data
