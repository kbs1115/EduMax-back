from enum import Enum

"""----------------------------------------------------------------------------"""


# query_param 정의

class PostSearchFilterParam(str, Enum):
    AUTHOR = "AUTHOR"
    CONTENT = "CONTENT"
    TITLE = "TITLE"
    TOTAL = "TOTAL"


class PostSortCategoryParam(str, Enum):
    CREATE_AT = "create_at"
    MOST_LIKE = "MOST_LIKE"


class PostCategoriesParam(str, Enum):
    FREE = "FR"
    NOTICE = "NO"
    KOREAN_QUESTION = "KQ"
    ENG_QUESTION = "EQ"
    MATH_QUESTION = "MQ"
    KOREAN_DATA = "KD"
    ENG_DATA = "ED"
    MATH_DATA = "MD"


"""----------------------------------------------------------------------------"""
