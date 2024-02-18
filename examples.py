import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from community.serializers import PostRetrieveSerializer, UserSerializer
from community.model.models import Post
from edumax_account.models import User
from django.utils import timezone

user1 = User.objects.get(id=1)
p = Post(id=1, title="1", content="c1", created_at=timezone.now(), author=user1)
serializer = PostRetrieveSerializer(p)
userSerializer = UserSerializer(user1)
returnDict = {}
returnDict.update(serializer.data)
returnDict.update(author=userSerializer.data)
print(returnDict)
json = JSONRenderer().render(returnDict)
print(json)
