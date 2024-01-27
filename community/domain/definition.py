from enum import Enum

from django.db import models

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

"""----------------------------------------------------------------------------"""


# categories
class PostCategories(models.TextChoices):
    FREE = "FR"
    NOTICE = "NO"
    KOREAN_QUESTION = "KQ"
    ENG_QUESTION = "EQ"
    MATH_QUESTION = "MQ"
    KOREAN_DATA = "KD"
    ENG_DATA = "ED"
    MATH_DATA = "MD"


TREE_STRUCTURE = {
    """
        <설명>
        - post의 category depth 트리 구조이다.
        - 현재 english 를 제외한 나머지 과목들은 children이 없으며 추후 추가될 예정이다.
        - 모든 posts는 각 트리의 리프 노드에 위치에 있다. 
    """
    # english
    "KO": [],
    "EN": ["SC", "SA", "GR"],
    "MA": [],

    # eng-depth2
    "SC": ["TB", "EBS", "SCM"],
    "SA": ["SAM"],
    "GR": ["PGR", "BGR"],

    # eng-depth3
    "TB": ["E0", "E1", "E2"],
    "SCM": ["H1", "H2"]
}


class CategoryDepth1(models.TextChoices):
    KOREAN = "KO"
    ENGLISH = "EN"
    MATH = "MA"


class CategoryDepth2(models.TextChoices):
    # children of ENGLISH
    SCHOOL_TEST = "SC"
    SAT = "SA"
    GRAMMAR = "GR"


class CategoryDepth3(models.TextChoices):
    # children of SCHOOL_TEST
    TEXTBOOK = "TB"
    EBS = "EBS"
    SCHOOL_MOCK_EXAM = "SCM"

    # children of SAT
    SAT_MOCK_EXAM = "SAM"

    # child of GRAMMAR
    POCKET_GRAMMAR = "PGR"
    BASIC_GRAMMAR = "BGR"


class CategoryDepth4(models.TextChoices):
    # children of TEXTBOOK
    ENGLISH0 = "E0"
    ENGLISH1 = "E1"
    ENGLISH2 = "E2"
    READING_COMPOSITION = "RC"

    # children of SCHOOL_MOCK_EXAM
    HIGH1 = "H1"
    HIGH2 = "H2"
