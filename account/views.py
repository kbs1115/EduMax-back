from rest_framework.views import APIView
from .serializers import *
from .services import *
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .validators import SignupParamModel, LoginParamModel, PatchUserModel
from pydantic import ValidationError


class UserAPIView(APIView):
    permission_classes = [permissions.IsAdminUser, UserPermission]

    def get(self, request):
        dataOfMe = UserService.get_serializer_data(request, None)
        res = Response(dataOfMe, status=status.HTTP_200_OK)

        return res

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

    def patch(self, request):
        try:
            e = PatchUserModel(**request.data)
        except ValidationError as e:
            raise exceptions.ParseError(str(e))

        if request.data["email"] == None and request.data["nickname"] == None:
            raise exceptions.ParseError("There is no data to update")

        updatedDataOfMe = UserService.update_user(request, None)
        res = Response(updatedDataOfMe, status=status.HTTP_200_OK)

        return res

    def delete(self, request):
        UserService.delete_user(request, None)
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class CertainUserAPIView(APIView):
    permission_classes = [permissions.IsAdminUser, UserPermission]

    def get(self, request, pk):
        userData = UserService.get_serializer_data(request, pk)
        res = Response(userData, status=status.HTTP_200_OK)

        return res

    def patch(self, request, pk):
        try:
            e = PatchUserModel(**request.data)
        except ValidationError as e:
            raise exceptions.ParseError(str(e))

        if request.data["email"] == None and request.data["nickname"] == None:
            raise exceptions.ParseError("There is no data to update")

        updatedUserData = UserService.update_me(request, pk)
        res = Response(updatedUserData, status=status.HTTP_200_OK)

        return res

    def delete(self, request, pk):
        UserService.delete_user(request, pk)
        return Response({}, status=status.HTTP_204_NO_CONTENT)


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
