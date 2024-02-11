from functools import wraps
from typing import Type, Union
from django.http import JsonResponse, QueryDict
from rest_framework import status, exceptions
from pydantic import BaseModel, Field

from community.domain.definition import *

"""validator에 사용되는 임시 model class"""


# post view 에 들어오는 query_param을 validate 하기위한 임의의 model
class PostQueryParam(BaseModel):
    page: int = Field(default=1, ge=1)
    category: PostCategoriesParam = Field(default=PostCategoriesParam.ENG_QUESTION)
    search_filter: PostSearchFilterParam = Field(default=PostSearchFilterParam.TOTAL)
    q: str = Field(default=None)
    sort: PostSortCategoryParam = Field(default=PostSortCategoryParam.CREATED_AT)


class PostPathParam(BaseModel):
    post_id: int = Field(ge=0)


class CreatePostRequestBody(BaseModel):
    category: PostCategoriesParam = Field(default=PostCategoriesParam.ENG_QUESTION)
    content: str = Field(min_length=1)
    title: str = Field(max_length=30)
    html_content: str = Field(min_length=1)
    # files 도 valid 하면 좋을듯


class UpdatePostRequestBody(BaseModel):
    category: PostCategoriesParam = Field(default=None)
    content: str = Field(min_length=1, default=None)
    title: str = Field(max_length=30, default=None)
    html_content: str = Field(min_length=1, default=None)
    files_state: PostFilesState = Field(default=None)
    # files 도 valid 하면 좋을듯


"""----------------------------------------------------------------------------"""


class LectureQueryParam(BaseModel):
    page: int = Field(default=1, ge=1)
    category: Union[
        LectureCategoriesDepth1Param,
        LectureCategoriesDepth2Param,
        LectureCategoriesDepth3Param,
        LectureCategoriesDepth4Param,
    ] = Field(default=LectureCategoriesDepth1Param.ENGLISH)
    search_filter: LectureSearchFilterParam = Field(
        default=LectureSearchFilterParam.TOTAL
    )
    q: str = Field(default=None)


class LecturePathParam(BaseModel):
    lecture_id: int = Field(ge=0)


class CreateLectureRequestBody(BaseModel):
    category_d1: LectureCategoriesDepth1Param = Field(
        default=LectureCategoriesDepth1Param.ENGLISH
    )
    category_d2: LectureCategoriesDepth2Param = Field(default=None)
    category_d3: LectureCategoriesDepth3Param = Field(default=None)
    category_d4: LectureCategoriesDepth4Param = Field(default=None)
    youtube_id: str = Field(min_length=1)
    title: str = Field(max_length=30)


class UpdateLectureRequestBody(BaseModel):
    category_d1: LectureCategoriesDepth1Param = Field(default=None)
    category_d2: LectureCategoriesDepth2Param = Field(default=None)
    category_d3: LectureCategoriesDepth3Param = Field(default=None)
    category_d4: LectureCategoriesDepth4Param = Field(default=None)
    youtube_id: str = Field(min_length=1, default=None)
    title: str = Field(max_length=30, default=None)


"""----------------------------------------------------------------------------"""


class CreateCommentRequestBody(BaseModel):
    content: str = Field(min_length=1)
    html_content: str = Field(min_length=1)
    # files 도 valid 하면 좋을듯


class CommentPathParam(BaseModel):
    comment_id: int = Field(ge=0)


class UpdateCommentRequestBody(BaseModel):
    content: str = Field(min_length=1)
    html_content: str = Field(min_length=1)
    files_state: PostFilesState = Field(default=None)
    # files 도 valid 하면 좋을듯

    """validator 모음"""


# query_param validator
def validate_query_params(model: Type[BaseModel]):
    """
    <설명>
    정의된 query_param model 외의 query param 들은 모두 무시한다.
    validated_query_params에 validation한 param을 넘겨준다.
    """

    def decorated_func(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            request = args[1]
            params = request.GET.dict()
            try:
                validated_params = model.model_validate(params)
            except ValueError as e:
                raise exceptions.ParseError(str(e))

            return f(*args, **kwargs, validated_query_params=validated_params)

        return wrapper

    return decorated_func


# path_param validator
def validate_path_params(model: Type[BaseModel]):
    """
    <설명>
    만약 path_param이 없을시 에러
    잘못된 path_param일시 400 response를 return 한다.
    """

    def decorated_func(f):
        @wraps(f)
        def wrapper(
            *args, **kwargs
        ):  # url 캡처후 view로 보내주는 path_params 은 kwargs로 넘겨준다.
            try:
                model(**kwargs)
            except ValueError as e:
                raise exceptions.ParseError(str(e))
            return f(*args, **kwargs)

        return wrapper

    return decorated_func


def validate_body_request(model: Type[BaseModel]):
    """
    <설명>
    request의 body에 있는 데이터를 검증한다.

    """

    def decorated_func(f):
        @wraps(f)
        def wrapper(
            *args, **kwargs
        ):  # url 캡처후 view로 보내주는 path_params 은 kwargs로 넘겨준다.
            request = args[1]
            body_data = request.data
            if isinstance(body_data, QueryDict):
                body_data = body_data.dict()
            try:
                validated_params = model.model_validate(body_data)
            except ValueError as e:
                raise exceptions.ParseError(str(e))
            return f(*args, **kwargs, validated_request_body=validated_params)

        return wrapper

    return decorated_func
