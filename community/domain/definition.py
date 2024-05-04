from enum import Enum

import strenum as strenum
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
    ALL = "AL"  # 전체 SELECT 추가
    FREE = "FR"
    NOTICE = "NO"
    KOREAN_QUESTION = "KQ"
    ENG_QUESTION = "EQ"
    MATH_QUESTION = "MQ"
    TAMGU_QUESTION = "TQ"
    KOREAN_DATA = "KD"
    ENG_DATA = "ED"
    MATH_DATA = "MD"
    TAMGU_DATA = "TD"

    def __str__(self):
        return self.value


class PostFilesState(Enum):
    REPLACE = "REPLACE"
    DELETE = "DELETE"

    def __str__(self):
        return self.value


class LectureSearchFilterParam(Enum):
    # name 이 왼쪽, value 가 오른쪽
    AUTHOR = "AUTHOR"
    TITLE = "TITLE"
    TOTAL = "TOTAL"

    def __str__(self):
        return self.value


class LectureCategoriesDepth1Param(Enum):
    KOREAN = "KO"
    ENGLISH = "EN"
    MATH = "MA"
    TAMGU = "TM"

    def __str__(self):
        return self.value


class LectureCategoriesDepth2Param(Enum):
    # children of ENGLISH
    SCHOOL_TEST = "SC"
    SAT = "SA"
    GRAMMAR = "GR"

    # children of MATH
    CALCULUS = "CC"
    PROBABILITY_AND_STATIC = "PS"
    MATH_1 = "M1"
    MATH_2 = "M2"
    MATH_HIGH = "MH"

    def __str__(self):
        return self.value


class LectureCategoriesDepth3Param(Enum):
    # children of SCHOOL_TEST
    TEXTBOOK = "TB"
    EBS = "EBS"
    SCHOOL_MOCK_EXAM = "SCM"

    # children of SAT
    SAT_MOCK_EXAM = "SAM"

    # child of GRAMMAR
    POCKET_GRAMMAR = "PGR"
    BASIC_GRAMMAR = "BGR"

    def __str__(self):
        return self.value


class LectureCategoriesDepth4Param(Enum):
    # children of TEXTBOOK
    ENGLISH0 = "E0"
    ENGLISH1 = "E1"
    ENGLISH2 = "E2"
    READING_COMPOSITION = "RC"

    # children of SCHOOL_MOCK_EXAM
    HIGH1 = "H1"
    HIGH2 = "H2"

    def __str__(self):
        return self.value


"""----------------------------------------------------------------------------"""

# post list 의 페이지 size
POST_LIST_PAGE_SIZE = 10

"""----------------------------------------------------------------------------"""


# categories
class PostCategories(models.TextChoices):
    FREE = "FR"
    NOTICE = "NO"
    KOREAN_QUESTION = "KQ"
    ENG_QUESTION = "EQ"
    MATH_QUESTION = "MQ"
    TAMGU_QUESTION = "TQ"
    KOREAN_DATA = "KD"
    ENG_DATA = "ED"
    MATH_DATA = "MD"
    TAMGU_DATA = "TD"


TREE_STRUCTURE = {
    """
        <설명>
        - post의 category depth 트리 구조이다.
        - 현재 english 를 제외한 나머지 과목들은 children이 없으며 추후 추가될 예정이다.
        - 모든 posts는 각 트리의 리프 노드에 위치에 있다. 
    """
    # english, math
    "KO": [],
    "EN": ["SC", "SA", "GR"],
    "MA": ["CC", "PS", "M1", "M2", "MH"],
    "TM": [],
    # eng-depth2
    "SC": ["TB", "EBS", "SCM"],
    "SA": ["SAM"],
    "GR": ["PGR", "BGR"],
    # eng-depth3
    "TB": ["E0", "E1", "E2"],
    "SCM": ["H1", "H2"],
}


class CategoryDepth1(models.TextChoices):
    KOREAN = "KO"
    ENGLISH = "EN"
    MATH = "MA"
    TAMGU = "TM"


class CategoryDepth2(models.TextChoices):
    # children of ENGLISH
    SCHOOL_TEST = "SC"
    SAT = "SA"
    GRAMMAR = "GR"
    # children of MATH
    CALCULUS = "CC"
    PROBABILITY_AND_STATIC = "PS"
    MATH_1 = "M1"
    MATH_2 = "M2"
    MATH_HIGH = "MH"


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


"""----------------------------------------------------------------------------"""
# 영어유튜브 PLAYLIST(ID,TITLE)과 LECTURE CATEGORY의 매핑
"""
<H1>
2022년 고1 11월 모의고사 : PLVNEoWri1a_BIkcVoxJkgO4KmizomZ3MZ
2022년 고1 9월 모의고사 : PLVNEoWri1a_AqQgoYrwlyCJnC1GbHJtcj
2020년 고1 6월 모의고사 내신 : PLVNEoWri1a_CGsx9m2wKNi5iznhCro70l
2021년 고1 9월 모의고사 : PLVNEoWri1a_A7hafkCgqu0zSZpCb9B2wD
2022년 고1 3월 모의고사 :PLVNEoWri1a_BBMFWe8VqAYBGf0XuHBloG
2021년 고1 3월 모의고사 : PLVNEoWri1a_ATV7-K1BWq0VjjmLT9VTyq
2021년 고1 6월 모의고사 : PLVNEoWri1a_DkJo6yC7xETF10Tnx5wN-v

<H2>
2023년 고2 3월 모의고사 : PLVNEoWri1a_DnRId9U4C3fcEvO2dPwvR6
2021년 고2 11월 모의고사 : PLVNEoWri1a_DjdYBf7uxR3BPsDINFPZvy
2022년 고2 9월 모의고사 : PLVNEoWri1a_AE2EL89j9r-7RwFsRpBm9B
2021년 고2 9월 모의고사 : PLVNEoWri1a_A6ncPlmPa2cm3cIJwFDWkt
2019년 고2 3월 모의고사 : PLVNEoWri1a_Bzndf0Uz_2m9EBVyIR_Mva
2020년 고2 3월 모의고사: PLVNEoWri1a_CrhBd5i6yGjkehmYYMduQf
2021년 고2 3월 모의고사 : PLVNEoWri1a_Cm-xI8z-W821X_YLL9N0bv
2022년 고2 3월 모의고사 : PLVNEoWri1a_AaUmziV5in0-YukM7UPZip
2021년 고2 6월 모의고사 :PLVNEoWri1a_AuSJZibtH430hUF_JUYt4K
고2 기출어법 즉석풀기 : PLVNEoWri1a_A1tUrM1m33OukriG3oE3Yq


<PGR>
호주머니어법 : PLVNEoWri1a_Bak36K4uBE15jNxIbF_C9i

<BGR>
기초영어 문법 : PLVNEoWri1a_C7_qu8cdcF46zeUEwy4gtE

<SAM>
2022년 고3 6월 모의고사: PLVNEoWri1a_C2HFu-yTE9bFtuu7znlV9G
2022년 고3 3월 모의고사: PLVNEoWri1a_BMMK__PGQ1LMujoj5XsKKE
2020년 고3 6월 모의고사 : PLVNEoWri1a_BiWB5H5i_rWCUqRquT0cBI
3등급 이하인 학생이 수능 1,2등급 받는방법 : PLVNEoWri1a_APk4ElPjzvZXc0_uozd0AU
패턴영어1 : PLVNEoWri1a_BzLR8d-ybEgsJgL1lNLPuU

<E1>
영어1 시사한 내신: PLVNEoWri1a_Ctmb7zC9TDsGnmEByv28pr
영어1 비상 홍 : PLVNEoWri1a_CGMszGfPX9agJm2o2C15MA
영어1 시사박 내신 :PLVNEoWri1a_B63PG1T8CY5ppcERaR_dBf

<E2>
영어2 시사박 내신: PLVNEoWri1a_DHJLgXOucc5Y6aqX0glxjq

<E0>
영어권문화 : PLVNEoWri1a_CEfAYln7MuGsu5Tou9XzYO
진로영어 시사박 : PLVNEoWri1a_BCU5W6kaK00RA8bMpwAsUa


<EBS
올림포스1 : PLVNEoWri1a_Az5p0_3UUmbH13y4VKoKCC
수특라이트 1,2,7,8,9,19강 내신대비 : PLVNEoWri1a_Dnjt5lH0h2GkZi8S8zVhmD
2022 ebs 수특 영어내신대비 : PLVNEoWri1a_CY4V8w5-v9sBNlqLrqlhaV
올림포스2 : PLVNEoWri1a_Aonp4LemUe7vR14CYqDrKL

"""

# 계층별 나올수있는 경우의수
CATEGORY_DEPTH_LIST = [
    # D1    D2    D3     D4
    ["EN", "SC", "SCM", "H1"],
    ["EN", "SC", "SCM", "H2"],
    ["EN", "GR", "PGR", None],
    ["EN", "GR", "BGR", None],
    ["EN", "SA", "SAM", None],
    ["EN", "SC", "TB", "E1"],
    ["EN", "SC", "TB", "E2"],
    ["EN", "SC", "TB", "E0"],
    ["EN", "SC", "EBS", None],
    ["MA", "CC", None, None],
    ["MA", "PS", None, None],
    ["MA", "M1", None, None],
    ["MA", "M2", None, None],
    ["MA", "MH", None, None]
]

# LECTURE CATEGORY와 PLAYLIST ID 관계 DICT
# 시간복잡도를 위해서 playlist id를 가지고 category를 찾게 만듦
PLAYLIST_ID_KEY_CATEGORY_VALUE = {
    # 영어
    # H1
    "PLVNEoWri1a_BIkcVoxJkgO4KmizomZ3MZ": CATEGORY_DEPTH_LIST[0],
    "PLVNEoWri1a_AqQgoYrwlyCJnC1GbHJtcj": CATEGORY_DEPTH_LIST[0],
    "PLVNEoWri1a_CGsx9m2wKNi5iznhCro70l": CATEGORY_DEPTH_LIST[0],
    "PLVNEoWri1a_A7hafkCgqu0zSZpCb9B2wD": CATEGORY_DEPTH_LIST[0],
    "PLVNEoWri1a_BBMFWe8VqAYBGf0XuHBloG": CATEGORY_DEPTH_LIST[0],
    "PLVNEoWri1a_ATV7-K1BWq0VjjmLT9VTyq": CATEGORY_DEPTH_LIST[0],
    "PLVNEoWri1a_DkJo6yC7xETF10Tnx5wN-v": CATEGORY_DEPTH_LIST[0],

    # H2
    "PLVNEoWri1a_DnRId9U4C3fcEvO2dPwvR6": CATEGORY_DEPTH_LIST[1],
    "PLVNEoWri1a_DjdYBf7uxR3BPsDINFPZvy": CATEGORY_DEPTH_LIST[1],
    "PLVNEoWri1a_AE2EL89j9r-7RwFsRpBm9B": CATEGORY_DEPTH_LIST[1],
    "PLVNEoWri1a_A6ncPlmPa2cm3cIJwFDWkt": CATEGORY_DEPTH_LIST[1],
    "PLVNEoWri1a_Bzndf0Uz_2m9EBVyIR_Mva": CATEGORY_DEPTH_LIST[1],
    "PLVNEoWri1a_CrhBd5i6yGjkehmYYMduQf": CATEGORY_DEPTH_LIST[1],
    "PLVNEoWri1a_Cm-xI8z-W821X_YLL9N0bv": CATEGORY_DEPTH_LIST[1],
    "PLVNEoWri1a_AaUmziV5in0-YukM7UPZip": CATEGORY_DEPTH_LIST[1],
    "PLVNEoWri1a_AuSJZibtH430hUF_JUYt4K": CATEGORY_DEPTH_LIST[1],
    "PLVNEoWri1a_A1tUrM1m33OukriG3oE3Yq": CATEGORY_DEPTH_LIST[1],

    # PGR
    "PLVNEoWri1a_Bak36K4uBE15jNxIbF_C9i": CATEGORY_DEPTH_LIST[2],

    # BGR
    "PLVNEoWri1a_C7_qu8cdcF46zeUEwy4gtE": CATEGORY_DEPTH_LIST[3],

    # SAM
    "PLVNEoWri1a_C2HFu-yTE9bFtuu7znlV9G": CATEGORY_DEPTH_LIST[4],
    "PLVNEoWri1a_BMMK__PGQ1LMujoj5XsKKE": CATEGORY_DEPTH_LIST[4],
    "PLVNEoWri1a_BiWB5H5i_rWCUqRquT0cBI": CATEGORY_DEPTH_LIST[4],
    "PLVNEoWri1a_APk4ElPjzvZXc0_uozd0AU": CATEGORY_DEPTH_LIST[4],
    "PLVNEoWri1a_BzLR8d-ybEgsJgL1lNLPuU": CATEGORY_DEPTH_LIST[4],

    # H1
    "PLVNEoWri1a_Ctmb7zC9TDsGnmEByv28pr": CATEGORY_DEPTH_LIST[5],
    "PLVNEoWri1a_CGMszGfPX9agJm2o2C15MA": CATEGORY_DEPTH_LIST[5],
    "PLVNEoWri1a_B63PG1T8CY5ppcERaR_dBf": CATEGORY_DEPTH_LIST[5],

    # E2
    "PLVNEoWri1a_DHJLgXOucc5Y6aqX0glxjq": CATEGORY_DEPTH_LIST[6],

    # E0
    "PLVNEoWri1a_CEfAYln7MuGsu5Tou9XzYO": CATEGORY_DEPTH_LIST[7],
    "PLVNEoWri1a_BCU5W6kaK00RA8bMpwAsUa": CATEGORY_DEPTH_LIST[7],

    # EBS
    "PLVNEoWri1a_Az5p0_3UUmbH13y4VKoKCC": CATEGORY_DEPTH_LIST[8],
    "PLVNEoWri1a_Dnjt5lH0h2GkZi8S8zVhmD": CATEGORY_DEPTH_LIST[8],
    "PLVNEoWri1a_CY4V8w5-v9sBNlqLrqlhaV": CATEGORY_DEPTH_LIST[8],
    "PLVNEoWri1a_Aonp4LemUe7vR14CYqDrKL": CATEGORY_DEPTH_LIST[8],

    # 수학유튜브 PLAYLIST, CATOEGORY 매핑
    "PLC7mOOjykyW_9jMWqwHh_jcmud8hW91om": CATEGORY_DEPTH_LIST[13],
    # M2
    "PLC7mOOjykyW-B6sB_DFOvR0OdiVQdDrSa": CATEGORY_DEPTH_LIST[12],
    # M1
    "PLC7mOOjykyW9o0at7hQNKTUyStVYuLIuC": CATEGORY_DEPTH_LIST[11],
    # PS
    "PLC7mOOjykyW-ZkxpTTcw1AowXl6yIvIzB": CATEGORY_DEPTH_LIST[10],
    # CC
    "PLC7mOOjykyW_l8uOAOdL_vTPFSEVHpiey": CATEGORY_DEPTH_LIST[9]
}
