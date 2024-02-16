from rest_framework import exceptions

from account.models import EmailTemporaryKey, PwChangeTemporaryQueryParam


def validate_email_key(email, auth_key):
    """
    email을 기준으로 임시키를 저장한 db를 확인후
    가장 최근키를 기준으로 키의 유효성을 판단한다.(여러번 요청했을수도 있기때문에)
    """
    queryset = EmailTemporaryKey.objects.filter(email=email)
    if queryset.exists():
        email_key_instance = queryset.latest('created_at')
        if email_key_instance.key == auth_key:
            return True
        else:
            raise exceptions.ValidationError(
                "인증번호가 틀렸습니다."
            )
    else:
        raise exceptions.ValidationError(  # 물론 이부분은 프론트에서도 이메일 전송을 안누르면 인증하기를 불가능하게 만들어놔야함
            "이메일 시간이 만료됐거나, 이메일 전송이 필요합니다."
        )


def create_email_key_model_instance(email, auth_key):
    """
    이메일 인증을 위한 임시키 db 저장
    """
    return EmailTemporaryKey.objects.create(email=email, key=auth_key)


def create_password_change_param_model_inst(email, random_query_params):
    """
    user/pw-change/?verify= 에 해당하는 쿼리 파라매터 임시저장
    """
    return PwChangeTemporaryQueryParam.objects.create(email=email, query_param=random_query_params)
