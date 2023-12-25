from django.test import TestCase, TransactionTestCase

from .models import Post
from account.models import User

from django.utils import timezone


class PostModelTests(TransactionTestCase):
    def setUp(self):
        User.objects.create(
            username="TestUser1", nickname="T1", email="testtest1@gmail.com"
        )

    def test_Post_title_length_less_than_30(self):
        user1 = User.objects.get(id=1)

        Post.objects.create(
            title="Test1Test1Test1Test1Test1Test1",
            content="testtest2",
            created_at=timezone.now(),
            author=user1,
        )
        p = Post.objects.get(title="Test1Test1Test1Test1Test1Test1")
        self.assertEqual(p.content, "testtest2")

        with self.assertRaises(Exception):
            Post.objects.create(
                title="Test1Test1Test1Test1Test1Test1!!!!",  # over length 30
                content="testtest3",
                created_at=timezone.now(),
                author=user1,
            )
