from account.serializers import *
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
    def create_user(data):
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return serializer.validated_data
        else:
            raise exceptions.ValidationError(serializer.errors)

    def check_duplicate_field_value(
            self,
            login_id=None,
            email=None,
            nickname=None
    ):
        if login_id is not None:
            return UserService.user_exists_with_field(User.USERNAME_FIELD, login_id)
        elif email is not None:
            return UserService.user_exists_with_field(User.EMAIL_FIELD, email)
        elif nickname is not None:
            return UserService.user_exists_with_field(User.NICKNAME_FIELD, nickname)
        else:
            raise exceptions.APIException("there is no field")


class UserService:
    @classmethod
    def user_exists_with_field(cls, field, value):
        if field == User.EMAIL_FIELD:
            return User.objects.filter(email=value).exists()
        elif field == User.NICKNAME_FIELD:
            return User.objects.filter(nickname=value).exists()
        elif field == User.USERNAME_FIELD:
            return User.objects.filter(login_id=value).exists()

    @classmethod
    def get_me(cls, request):
        user = request.user
        if user is None:
            raise exceptions.NotFound("user not found")

        return user

    @classmethod
    def get_user_with_pk(cls, pk):
        try:
            return User.objects.get(id=pk)
        except User.DoesNotExist:
            raise exceptions.NotFound("user not found")

    @classmethod
    def get_serializer_data(cls, user):
        serializer = UserSerializer(user)
        return serializer.data

    @classmethod
    def update_user(cls, user, data):
        serializer = UserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        else:
            raise exceptions.ValidationError(serializer.errors)

    @classmethod
    def delete_user(cls, user):
        try:
            user.delete()
        except:
            raise exceptions.APIException("deletion failed")


class AuthService:
    def loginService(data):
        user = authenticate(
            login_id=data.get("login_id"), password=data.get("password")
        )

        if user:
            serializer = UserSerializer(user)

            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)

            return {
                "userData": serializer.data,
                "refreshToken": refresh_token,
                "accessToken": access_token,
            }
        else:
            raise exceptions.ValidationError(
                "The provided information does not match any user."
            )
