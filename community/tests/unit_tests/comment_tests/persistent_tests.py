import pytest
from unittest.mock import Mock

from community.model.access import *
from .conftest import *


class TestAccessFunctions:
    @pytest.mark.django_db
    def test_get_post_from_id(self, comment_db_setup):
        comment_db_setup["user_instance"].save()
        comment_db_setup["post_instance"].save()

        instance = get_post_from_id(1)

        assert instance == comment_db_setup["post_instance"]

        with pytest.raises(NotFound):
            instance = get_post_from_id(2)

    @pytest.mark.django_db
    def test_get_parent_post_id(self, comment_db_setup):
        comment_db_setup["user_instance"].save()
        comment_db_setup["post_instance"].save()
        comment_db_setup["comment_instance"].save()

        post_id = get_parent_post_id(1)

        assert post_id == 1

        with pytest.raises(NotFound):
            post_id = get_parent_post_id(3)

    @pytest.mark.django_db
    def test_get_comment_user_id(self, comment_db_setup):
        comment_db_setup["user_instance"].save()
        comment_db_setup["post_instance"].save()
        comment_db_setup["comment_instance"].save()

        author_id = get_comment_user_id(1)

        assert author_id == 1

        with pytest.raises(NotFound):
            author_id = get_comment_user_id(5)

    @pytest.mark.django_db
    def test_get_comment_from_id(self, comment_db_setup):
        comment_db_setup["user_instance"].save()
        comment_db_setup["post_instance"].save()
        comment_db_setup["comment_instance"].save()

        comment = get_comment_from_id(1)

        assert comment == comment_db_setup["comment_instance"]

        with pytest.raises(NotFound):
            comment = get_comment_from_id(10)
