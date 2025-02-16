import requests, os
from dotenv import load_dotenv
from django.conf import settings
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import APIException, NotAuthenticated, NotFound
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from allauth.socialaccount.models import SocialAccount


from edumax_account.models import User
from edumax_account.serializers import UserSerializer
from edumax_account.model.user_access import (
    get_user_with_email,
    get_social_user_with_user,
)
from edumax_account.service.user_service import SignUpService, AuthService

load_dotenv(verbose=True)

BASE_URL = "http://edumax-kr.com/"
GOOGLE_CALLBACK_URI = BASE_URL + "login/google"


@api_view(["GET"])
def google_oauth_redirect(request):
    scope = "https://www.googleapis.com/auth/userinfo.email"
    client_id = os.getenv("SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    redirect_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}"
    )
    return Response({'redirect_url': redirect_url})


@api_view(["GET"])
def google_callback(request):
    client_id = os.environ.get("SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("SOCIAL_AUTH_GOOGLE_SECRET")
    code = request.GET.get("code")

    # 1. 받은 코드로 구글에 access token 요청
    token_req = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "authorization_code",
            "redirect_uri": GOOGLE_CALLBACK_URI,
        },
    )

    ### 1-1. json으로 변환 & 에러 부분 파싱
    token_req_json = token_req.json()
    error = token_req_json.get("error")

    ### 1-2. 에러 발생 시 종료
    if error is not None:
        raise APIException(error)

    ### 1-3. 성공 시 access_token 가져오기
    access_token = token_req_json.get("access_token")

    #################################################################

    # 2. 가져온 access_token으로 이메일값을 구글에 요청(나중에 Authorization header로 토큰 위치 변경)
    email_req = requests.get(
        f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}"
    )
    email_req_status = email_req.status_code

    ### 2-1. 에러 발생 시 400 에러 반환
    if email_req_status != 200:
        return NotAuthenticated("Cannot get email from google server")

    ### 2-2. 성공 시 이메일 가져오기
    email_req_json = email_req.json()
    email = email_req_json.get("email")

    ### 2-3. 이메일을 가져왔으므로 여기서 안전을 위해 토큰을 파기한다.(이후에 토큰 사용할 일이 없으므로)
    destroy_token_req = requests.post(
        f"https://oauth2.googleapis.com/revoke", data={"token": access_token}
    )
    if destroy_token_req.status_code != 200:
        raise APIException("Cannot destroy token")

    # 3. 전달받은 이메일, access_token, code를 바탕으로 회원가입/로그인
    try:
        user = get_user_with_email(email)
        social_user = get_social_user_with_user(user)

        if social_user.provider != "google":
            raise APIException("not a google email user")

        data = AuthService.social_login_service(user)
        res = Response(
            {
                "user": data["userData"],
                "message": "login success",
                "token": {
                    "access": data["accessToken"],
                    "refresh": data["refreshToken"],
                },
            },
            status=status.HTTP_200_OK,
        )
        res.set_cookie("refreshToken", data["refreshToken"], httponly=True)

        return res

    except SocialAccount.DoesNotExist:
        raise APIException("login to normal account")

    except:
        # 전달받은 이메일로 기존에 가입된 유저가 아예 없으면 => 새로 회원가입 & 해당 유저의 jwt 발급
        user = SignUpService.create_social_user(email)
        data = AuthService.social_login_service(user)
        res = Response(
            {
                "user": data["userData"],
                "message": "Signup and login success",
                "token": {
                    "access": data["accessToken"],
                    "refresh": data["refreshToken"],
                },
            },
            status=status.HTTP_200_OK,
        )
        res.set_cookie("refreshToken", data["refreshToken"], httponly=True)

        return res
