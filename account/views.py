from django.http import JsonResponse
from rest_framework.views import APIView
from account.service.user_service import *
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from community.view.validation import validate_body_request
from .validators import SignupParamModel, LoginParamModel, PatchUserModel, UserUniqueFieldModel, EmailFieldModel, \
    EmailCheckFieldModel
from pydantic import ValidationError


class UserAPIView(APIView):
    permission_classes = [UserPermission]

    def get_authenticated_user(self, request):
        user = UserService.get_me(request)
        self.check_object_permissions(request, user)
        return user

    def get(self, request):

        user = self.get_authenticated_user(request)

        data_of_me = UserService.get_serializer_data(user)
        res = Response(data_of_me, status=status.HTTP_200_OK)

        return res

    def post(self, request):
        try:
            e = SignupParamModel(**request.data)
        except ValidationError as e:
            raise exceptions.ParseError(str(e))

        user_data = SignUpService.create_user(request.data)

        res = Response(
            {
                "user": user_data,
                "message": "signup success",
            },
            status=status.HTTP_200_OK,
        )
        return res

    def patch(self, request):
        try:
            e = PatchUserModel(**request.data)
        except ValidationError as e:
            raise exceptions.ParseError("invalid data format")

        if request.data.get("email") is None and request.data.get("nickname") is None:
            raise exceptions.ParseError("invalid data format")

        user = self.get_authenticated_user(request)

        updated_data_of_me = UserService.update_user(user, request.data)
        res = Response(updated_data_of_me, status=status.HTTP_200_OK)

        return res

    def delete(self, request):
        user = self.get_authenticated_user(request)

        UserService.delete_user(user)
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class CertainUserAPIView(APIView):
    permission_classes = [UserPermission]

    def get_authenticated_user(self, request, pk):
        user = UserService.get_user_with_pk(pk)
        self.check_object_permissions(request, user)
        return user

    def get(self, request, pk):
        user = self.get_authenticated_user(request, pk)

        user_data = UserService.get_serializer_data(user)
        res = Response(user_data, status=status.HTTP_200_OK)

        return res

    def patch(self, request, pk):
        try:
            e = PatchUserModel(**request.data)
        except ValidationError as e:
            raise exceptions.ParseError("invalid data format")

        if request.data.get("email") is None and request.data.get("nickname") is None:
            raise exceptions.ParseError("invalid data format")

        user = self.get_authenticated_user(request, pk)

        updated_user_data = UserService.update_user(user, request.data)
        res = Response(updated_user_data, status=status.HTTP_200_OK)

        return res

    def delete(self, request, pk):
        user = self.get_authenticated_user(request, pk)

        UserService.delete_user(user)
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class AuthAPIView(APIView):
    def post(self, request):
        try:
            e = LoginParamModel(**request.data)
        except ValidationError as e:
            raise exceptions.ParseError("invalid data form")

        login_data = AuthService.loginService(request.data)

        res = Response(
            {
                "user": login_data["userData"],
                "message": "login success",
                "token": {
                    "access": login_data["accessToken"],
                    "refresh": login_data["refreshToken"],
                },
            },
            status=status.HTTP_200_OK,
        )
        res.set_cookie("refreshToken", login_data["refreshToken"], httponly=True)
        return res

    def delete(self, request):
        res = Response({"message": "logout success"}, status=status.HTTP_202_ACCEPTED)
        res.delete_cookie("refreshToken")
        return res


class DuplicateCheckerAPIView(APIView):
    @validate_body_request(UserUniqueFieldModel)
    def post(self, request, validated_request_body):
        field = {'login_id': validated_request_body.nickname,
                 'email': validated_request_body.login_id,
                 'nickname': validated_request_body.email}
        response = SignUpService().check_duplicate_field_value(**field)
        if response is True:
            return Response(status=status.HTTP_200_OK, data={"message": "duplicate"})
        elif response is False:
            return Response(status=status.HTTP_200_OK, data={"message": "no duplicate"})


class EmailSenderApiView(APIView):
    @validate_body_request(EmailFieldModel)
    def post(self, request, validated_request_body):
        email = {'email': validated_request_body.email}
        response = EmailService().send_email(**email)
        return JsonResponse(status=response.get("status_code"),
                            data={
                                "message": response.get("message", None),
                                "data": response.get("data", None)},
                            )


class EmailAuthenticationApiView(APIView):

    @validate_body_request(EmailCheckFieldModel)
    def post(self, request, validated_request_body):
        check = {
            'email': validated_request_body.email,
            'auth_key': validated_request_body.auth_key
        }
        response = EmailService().check_authentication(**check)
        return JsonResponse(status=response.get("status_code"),
                            data={
                                "message": response.get("message", None),
                                "data": response.get("data", None)},
                            )


class TestViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
