from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["login_id", "email", "nickname", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            login_id=validated_data["login_id"],
            email=validated_data["email"],
            nickname=validated_data["nickname"],
            password=validated_data["password"],
        )
        return user
