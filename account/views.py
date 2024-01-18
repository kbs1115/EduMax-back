from rest_framework.views import APIView
from .serializers import *
from .services import *
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .validators import SignupParamModel, LoginParamModel
from pydantic import ValidationError


class SignUpAPIView(APIView):
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


class AuthAPIView(APIView):
    def post(self, request):
        try:
            e = LoginParamModel(**request.data)
        except ValidationError as e:
            raise exceptions.ParseError("invalid data form")

        loginData = AuthService.loginService(request)
        userData = loginData["userData"]
        userData.pop("password", None)

        res = Response(
            {
                "user": userData,
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
