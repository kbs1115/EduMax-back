import pytest

from account.models import User
from community.models import Post


@pytest.fixture(scope='function')
def mocked_post_instance(mocker, monkeypatch):
    pass


class TestPostModel:
    pass


class TestCommentModel:
    pass


class TestAlarmModel:
    pass


class TestLikeModel:
    pass


class TestLectureModel:
    pass
