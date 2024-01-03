from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.middleware.csrf import get_token


class SignUpAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            res = Response(
                {
                    "user": serializer.validated_data,
                    "message": "signup success",
                },
                status=status.HTTP_200_OK,
            )
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthAPIView(APIView):
    def post(self, request):
        user = authenticate(
            login_id=request.data.get("login_id"), password=request.data.get("password")
        )

        if user is not None:
            serializer = UserSerializer(user)

            token = TokenObtainPairSerializer.get_token(user)
            refreshToken = str(token)
            accessToken = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "login success",
                    "token": {
                        "access": accessToken,
                        "refresh": refreshToken,
                    },
                },
                status=status.HTTP_200_OK,
            )
            res.set_cookie("refreshToken", refreshToken, httponly=True)
            return res
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        res = Response({"message": "Logout success"}, status=status.HTTP_202_ACCEPTED)
        res.delete_cookie("refreshToken")
        return res
