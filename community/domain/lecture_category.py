from django.db import models


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
    # english
    "KOREAN": [],
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


# 12.31 수정: 카테고리 depth 3,4 추가
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