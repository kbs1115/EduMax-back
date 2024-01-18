from rest_framework.views import APIView
from .serializers import *
from .services import *
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .validators import SignupParamModel, LoginParamModel
from pydantic import ValidationError


class UserAPIView(APIView):
    permission_classes = [permissions.IsAdminUser, UserPermission]

    def post(self, request):
        try:
            e = SignupParamModel(**request.data)
        except ValidationError as e:
            raise exceptions.ParseError(str(e))

        userData = SignUpService.get_user_data(request)

        res = Response(
            {
                "user": userData,
                "message": "signup success",
            },
            status=status.HTTP_200_OK,
        )
        return res

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)

        res = Response(serializer.data, status=status.HTTP_200_OK)
        return res


class CertainUserAPIView(APIView):
    permission_classes = [permissions.IsAdminUser, UserPermission]

    def get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise exceptions.NotFound("user not found")

    def get(self, request, pk):
        user = self.get_user(pk)
        serializer = UserSerializer(user)

        res = Response(serializer.data, status=status.HTTP_200_OK)
        return res

    def put(self, request, pk):
        user = self.get_user(pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_user(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AuthAPIView(APIView):
    def post(self, request):
        try:
            e = LoginParamModel(**request.data)
        except ValidationError as e:
            raise exceptions.ParseError("invalid data form")

        loginData = AuthService.loginService(request)

        res = Response(
            {
                "user": loginData["userData"],
                "message": "login success",
                "token": {
                    "access": loginData["accessToken"],
                    "refresh": loginData["refreshToken"],
                },
            },
            status=status.HTTP_200_OK,
        )
        res.set_cookie("refreshToken", loginData["refreshToken"], httponly=True)
        return res

    def delete(self, request):
        res = Response({"message": "logout success"}, status=status.HTTP_202_ACCEPTED)
        res.delete_cookie("refreshToken")
        return res


class TestViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
