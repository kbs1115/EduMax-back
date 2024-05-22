from .models import User, EmailTemporaryKey
from rest_framework import serializers
from allauth.socialaccount.models import SocialAccount


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["login_id", "email", "nickname", "password", "is_staff"]
        extra_kwargs = {"password": {"write_only": True}}

    def __init__(self, *args, **kwargs):
        # 'fields' 키워드를 통해 가져오고 싶은 필드들을 받음
        fields = kwargs.pop('fields', None)
        super(UserSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def create(self, validated_data):
        user = User.objects.create_user(
            login_id=validated_data["login_id"],
            email=validated_data["email"],
            nickname=validated_data["nickname"],
            password=validated_data["password"],
        )
        return user

    # 여기서는 user의 email, nickname만 업데이트한다.
    def update(self, instance, validated_data):
        instance.email = validated_data.get("email", instance.email)
        instance.nickname = validated_data.get("nickname", instance.nickname)
        instance.save()
        return instance


class SocialAccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialAccount
        fields = "__all__"
