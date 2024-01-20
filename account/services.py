from .serializers import *
from rest_framework import exceptions, permissions
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return not request.user.is_authenticated
        else:
            return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user:
            if obj.id == request.user.id:
                return True
            raise exceptions.PermissionDenied()
        raise exceptions.NotAuthenticated()


class SignUpService:
    def get_user_data(request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return serializer.validated_data
        else:
            raise exceptions.ValidationError(serializer.errors)


class UserService:
    def get_user(self, view, request, pk):
        if pk:
            user = self.get_user_with_pk(pk)
        else:
            user = self.get_me(request)
        view.check_object_permissions(request, user)
        return user

    def get_me(self, request):
        user = request.user
        if user is None:
            raise exceptions.NotFound("user not found")

        return user

    def get_user_with_pk(self, pk):
        try:
            return User.objects.get(id=pk)
        except User.DoesNotExist:
            raise exceptions.NotFound("user not found")

    def get_serializer_data(self, view, request, pk):
        user = self.get_user(view, request, pk)
        serializer = UserSerializer(user)
        return serializer.data

    def update_user(self, view, request, pk):
        user = self.get_user(view, request, pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        else:
            raise exceptions.ValidationError(serializer.errors)

    def delete_user(self, view, request, pk):
        user = self.get_user(view, request, pk)
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
