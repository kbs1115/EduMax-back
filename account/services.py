from .serializers import *
from rest_framework import exceptions
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class SignUpService:
    def get_user_data(request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return serializer.validated_data
        else:
            raise exceptions.ParseError("InvalidDataError")


class AuthService:
    def loginService(request):
        user = authenticate(
            login_id=request.data.get("login_id"), password=request.data.get("password")
        )

        if user:
            serializer = UserSerializer(user)

            token = TokenObtainPairSerializer.get_token(user)
            refreshToken = str(token)
            accessToken = str(token.access_token)

            return {
                "userData": serializer.data,
                "refreshToken": refreshToken,
                "accessToken": accessToken,
            }
        else:
            raise exceptions.ParseError("InvalidUserError")
