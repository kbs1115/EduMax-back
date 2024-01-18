from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["login_id", "email", "nickname", "password"]
        extra_kwargs = {"password": {"write_only": True}}

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
