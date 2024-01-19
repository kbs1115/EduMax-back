from .serializers import *
from rest_framework import exceptions, permissions
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method is "POST":
            return not request.user
        else:
            return request.user

    def has_object_permission(self, request, view, obj):
        if request.method is "POST":
            return True
        else:
            return request.user == obj


class SignUpService:
    def get_user_data(request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return serializer.validated_data
        else:
            raise exceptions.ValidationError(serializer.errors)


class UserService:
    def get_user(self, request, pk):
        if pk:
            return self.get_user_with_pk(pk)
        else:
            return self.get_me(request)

    def get_me(request):
        user = request.user
        if user is None:
            raise exceptions.NotFound("user not found")

        return user

    def get_user_with_pk(pk):
        try:
            return User.objects.get(id=pk)
        except User.DoesNotExist:
            raise exceptions.NotFound("user not found")

    def get_serializer_data(self, request, pk):
        user = self.get_user(request, pk)
        serializer = UserSerializer(user)
        return serializer.data

    def update_user(self, request, pk):
        user = self.get_user(request, pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        else:
            raise exceptions.ValidationError(serializer.errors)

    def delete_user(self, request, pk):
        user = self.get_user(request, pk)
        try:
            user.delete()
        except:
            raise exceptions.APIException("deletion failed")


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
            raise exceptions.ValidationError(
                "The provided information does not match any user."
            )
