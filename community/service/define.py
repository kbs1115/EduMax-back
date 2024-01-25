from enum import Enum

"""----------------------------------------------------------------------------"""


# query_param 정의

class PostSearchFilterParam(Enum):
    # name 이 왼쪽, value 가 오른쪽
    AUTHOR = "AUTHOR"
    CONTENT = "CONTENT"
    TITLE = "TITLE"
    TOTAL = "TOTAL"

    def __str__(self):
        return self.value


class PostSortCategoryParam(Enum):
    CREATED_AT = "created_at"
    MOST_LIKE = "MOST_LIKE"

    def __str__(self):
        return self.value


class PostCategoriesParam(Enum):
    FREE = "FR"
    NOTICE = "NO"
    KOREAN_QUESTION = "KQ"
    ENG_QUESTION = "EQ"
    MATH_QUESTION = "MQ"
    KOREAN_DATA = "KD"
    ENG_DATA = "ED"
    MATH_DATA = "MD"

    def __str__(self):
        return self.value


class PostFilesState(Enum):
    REPLACE = "REPLACE"
    DELETE = "DELETE"

    def __str__(self):
        return self.value


"""----------------------------------------------------------------------------"""

# post list 의 페이지 size
POST_LIST_PAGE_SIZE = 15
