from rest_framework.views import APIView
from .serializers import *
from .services import *
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class SignUpAPIView(APIView):
    def post(self, request):
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
        res = Response({"message": "Logout success"}, status=status.HTTP_202_ACCEPTED)
        res.delete_cookie("refreshToken")
        return res


class TestViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
