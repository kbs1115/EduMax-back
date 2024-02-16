from rest_framework.views import APIView

from account.model.user_access import get_user_with_pk
from account.service.user_service import *
from rest_framework import status, viewsets, permissions, exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from community.view.validation import validate_body_request, validate_query_params
from account.validators import SignupParamModel, LoginParamModel, PatchUserModel, UserUniqueFieldModel, \
    EmailCheckFieldModel, PasswordPageQueryParamModel, PasswordModel
from pydantic import ValidationError


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
        # EmailService().check_authentication()
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
        user = get_user_with_pk(pk=pk)
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


class GetLoginIdApiView(APIView):
    """
    비로그인 유저가 user instance를 요청할때
    이메일 인증을 통해 USER의 로그인 아이디를 알려준다.
    """

    @validate_body_request(EmailCheckFieldModel)
    def post(self, request, validated_request_body):
        check = {
            'email': validated_request_body.email,
            'auth_key': validated_request_body.auth_key
        }
        user_inst = UserService.get_user_with_email_auth(**check)
        return Response(status=status.HTTP_200_OK,
                        data={
                            "message": "email authenticate successfully",
                            "data": {"login_id": user_inst.login_id}
                        }
                        )


class RedirectPwChangeApiView(APIView):
    """
    비로그인 유저가 PASSWORD 변경을 요청할때
    이메일 인증을 통해서 PASSWORD 변경 페이지의 엔드포인트를 제공한다.
    """

    @validate_body_request(EmailCheckFieldModel)
    def post(self, request, validated_request_body):
        check = {
            'email': validated_request_body.email,
            'auth_key': validated_request_body.auth_key
        }
        random_query_param = UserService().make_random_query_param_with_email_auth(**check)
        return Response(status=status.HTTP_200_OK,
                        data={
                            "message": "email authenticate successfully",
                            "data": {"redirect_url": f"user/pw-change/?verify={random_query_param}"}
                        }
                        )


class PasswordChangeApiView(APIView):
    """
    패스워드 변경을 위한 API
    """

    @validate_body_request(PasswordModel)
    @validate_query_params(PasswordPageQueryParamModel)
    def post(self, request, validated_query_params, validated_request_body):
        new_pw = {'pw': validated_request_body.new_pw, "email": validated_request_body.email}
        UserService().change_password(**new_pw)
        return Response(status=status.HTTP_200_OK,
                        data={
                            "message": "password change successfully"
                        }
                        )


class AuthAPIView(APIView):
    def post(self, request):
        try:
            e = LoginParamModel(**request.data)
        except ValidationError as e:
            raise exceptions.ParseError("invalid data form")


        login_data = AuthService().loginService(request.data)

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
    """
    회원가입시 필수 필드 중복체크 확인에 쓰인다.
    """

    @validate_body_request(UserUniqueFieldModel)
    def post(self, request, validated_request_body):
        field = {'login_id': validated_request_body.nickname,
                 'email': validated_request_body.login_id,
                 'nickname': validated_request_body.email}
        response = SignUpService.check_duplicate_field_value(**field)
        if response is True:
            return Response(status=status.HTTP_200_OK, data={"message": "duplicate"})
        elif response is False:
            return Response(status=status.HTTP_200_OK, data={"message": "no duplicate"})


class TestViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
