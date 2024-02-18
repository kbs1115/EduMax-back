import pytest
from edumax_account.tests.conftests import *
from edumax_account.models import User
from edumax_account.serializers import UserSerializer
from rest_framework.validators import UniqueValidator


class TestUserSerializer:
    def test_model_serialization(self, user_instance):
        serializer = UserSerializer(user_instance)

        assert serializer.data == {
            "login_id": "kbs1115",
            "email": "bruce1115@naver.com",
            "nickname": "KKKBBBSSS",
        }

    def test_model_deserialization(self, valid_serialized_data, mocker):
        serializer = UserSerializer(data=valid_serialized_data)
        mocker.patch.object(
            UniqueValidator, "__call__"
        )  # unique 조건을 test하는 Validator의 __call__ method를 mocking한다.

        assert serializer.is_valid()
        assert serializer.errors == {}

    def test_model_deserialization_invalid(self, invalid_serialized_data, mocker):
        # login_id가 지나치게 긴 경우를 대표로 테스트함.
        serializer = UserSerializer(data=invalid_serialized_data)
        mocker.patch.object(
            UniqueValidator, "__call__"
        )  # unique 조건을 test하는 Validator의 __call__ method를 mocking한다.

        assert serializer.is_valid() == False
        assert serializer.errors != {}
