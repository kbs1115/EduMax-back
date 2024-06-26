from functools import wraps
from typing import Type, ClassVar, Union
from rest_framework import exceptions
from pydantic import BaseModel, Field, field_validator, model_validator

from community.domain.definition import *
import bleach

"""validator에 사용되는 임시 model class"""


# post view 에 들어오는 query_param을 validate 하기위한 임의의 model
class PostQueryParam(BaseModel):
    PAGE: ClassVar[str] = "page"
    CATEGORY: ClassVar[str] = "category"
    SEARCH_FILTER: ClassVar[str] = "search_filter"
    Q: ClassVar[str] = "q"
    SORT: ClassVar[str] = "sort"

    page: int = Field(default=1, ge=1)
    category: PostCategoriesParam = Field(default=PostCategoriesParam.ENG_QUESTION)
    search_filter: PostSearchFilterParam = Field(default=PostSearchFilterParam.TOTAL)
    q: str = Field(default=None)
    sort: PostSortCategoryParam = Field(default=PostSortCategoryParam.CREATED_AT)


class PostPathParam(BaseModel):
    post_id: int = Field(gt=0)


class CreatePostRequestBody(BaseModel):
    CATEGORY: ClassVar[str] = "category"
    CONTENT: ClassVar[str] = "content"
    TITLE: ClassVar[str] = "title"
    HTML_CONTENT: ClassVar[str] = "html_content"

    category: PostCategoriesParam = Field(default=PostCategoriesParam.ENG_QUESTION)
    content: str = Field(min_length=1)
    title: str = Field(max_length=30)
    html_content: str = Field(min_length=1)

    @model_validator(mode='before')
    @classmethod
    def sanitize_all_fields(cls, values):
        for field, value in values.items():
            if isinstance(value, str):
                values[field] = sanitize_html(value)
        return values


class UpdatePostRequestBody(BaseModel):
    CATEGORY: ClassVar[str] = "category"
    CONTENT: ClassVar[str] = "content"
    TITLE: ClassVar[str] = "title"
    HTML_CONTENT: ClassVar[str] = "html_content"
    FILES_STATE: ClassVar[str] = "files_state"

    category: PostCategoriesParam = Field(default=None)
    content: str = Field(min_length=1, default=None)
    title: str = Field(max_length=30, default=None)
    html_content: str = Field(min_length=1, default=None)
    files_state: PostFilesState = Field(default=None)

    @model_validator(mode='before')
    @classmethod
    def sanitize_all_fields(cls, values):
        for field, value in values.items():
            if isinstance(value, str):
                values[field] = sanitize_html(value)
        return values
    # files 도 valid 하면 좋을듯


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


class AlarmQueryParam(BaseModel):
    PAGE: ClassVar[str] = "page"

    page: int = Field(default=1, ge=1)


class MyCommentQueryParam(BaseModel):
    PAGE: ClassVar[str] = "page"
    Q: ClassVar[str] = "q"

    page: int = Field(default=1, ge=1)
    q: str = Field(default=None)


"""----------------------------------------------------------------------------"""


class CreateCommentRequestBody(BaseModel):
    content: str = Field(min_length=1)
    html_content: str = Field(min_length=1)

    @model_validator(mode='before')
    @classmethod
    def sanitize_all_fields(cls, values):
        for field, value in values.items():
            if isinstance(value, str):
                values[field] = sanitize_html(value)
        return values
    # files 도 valid 하면 좋을듯


class CommentPathParam(BaseModel):
    comment_id: int = Field(ge=0)


class MyCommentPathParam(BaseModel):
    page: int = Field(ge=0)


class UpdateCommentRequestBody(BaseModel):
    content: str = Field(min_length=1)
    html_content: str = Field(min_length=1)
    files_state: PostFilesState = Field(default=None)

    @model_validator(mode='before')
    @classmethod
    def sanitize_all_fields(cls, values):
        for field, value in values.items():
            if isinstance(value, str):
                values[field] = sanitize_html(value)
        return values

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
    request의 body에 있는 데이터를 검증한다.
    """

    def decorated_func(f):
        @wraps(f)
        def wrapper(
                *args, **kwargs
        ):
            request = args[1]
            body_data = request.data.dict()

            try:
                validated_params = model.model_validate(body_data)
            except ValueError as e:
                raise exceptions.ParseError(str(e))
            return f(*args, **kwargs, validated_request_body=validated_params)

        return wrapper

    return decorated_func


def sanitize_html(html_content):
    # 허용된 태그와 속성 정의
    allowed_tags = [
        'p', 'br', 'div', 'span', 'img', 'a', 'ul', 'ol', 'li', 'strong', 'em', 'blockquote'
    ]
    allowed_attributes = {
        '*': ['class', 'style'],
        'a': ['href', 'title'],
        'img': ['src', 'alt']
    }

    # HTML 콘텐츠를 sanitize
    cleaned_html = bleach.clean(
        html_content,
        tags=allowed_tags,
        attributes=allowed_attributes,
        strip=True  # 허용되지 않은 태그를 제거하고 내용만 남김
    )

    return cleaned_html


def reject_html_content(value: str) -> str:
    """
    입력된 문자열에서 HTML 태그가 포함되어 있는지 검사하고,
    HTML 태그가 있으면 예외를 발생시킵니다.
    """
    allowed_tags = []  # 허용할 태그를 비워 두어 모든 태그를 제거
    clean_value = bleach.clean(value, tags=allowed_tags, strip=True)
    if clean_value != value:
        raise ValueError("HTML content is not allowed.")
    return clean_value
