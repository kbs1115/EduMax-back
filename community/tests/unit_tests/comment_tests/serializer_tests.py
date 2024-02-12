import pytest
from rest_framework.validators import UniqueValidator
from rest_framework.relations import PrimaryKeyRelatedField

from community.serializers import CommentCreateSerializer, CommentRetrieveSerializer


# 현재 CommentCreateSerializer로는 deserialization만 수행하므로 해당 동작만 테스트한다.
class TestCommentCreateSerializer:
    def test_model_deserialization(
        self, valid_serialized_comment_data, comment_instance, mocker
    ):
        # DB에 접근하는 동작을 mocking한다.
        mocker.patch.object(UniqueValidator, "__call__")
        mocker.patch.object(PrimaryKeyRelatedField, "to_internal_value")

        serializer = CommentCreateSerializer(data=valid_serialized_comment_data[0])
        assert serializer.is_valid()
        assert serializer.errors == {}

        serializer = CommentCreateSerializer(data=valid_serialized_comment_data[1])
        assert serializer.is_valid()
        assert serializer.errors == {}

        serializer = CommentCreateSerializer(
            comment_instance, data={"content": "updatedtestcontent"}, partial=True
        )
        assert serializer.is_valid()
        assert serializer.errors == {}
        assert serializer.validated_data == {"content": "updatedtestcontent"}

    def test_invalid_model_deserialization(
        self, invalid_serialized_comment_data, comment_instance, mocker
    ):
        # DB에 접근하는 동작을 mocking한다.
        mocker.patch.object(UniqueValidator, "__call__")
        mocker.patch.object(PrimaryKeyRelatedField, "to_internal_value")

        serializer = CommentCreateSerializer(data=invalid_serialized_comment_data[0])
        assert serializer.is_valid() == False
        assert serializer.errors != {}

        serializer = CommentCreateSerializer(data=invalid_serialized_comment_data[1])
        assert serializer.is_valid() == False
        assert serializer.errors != {}

        # 잘못된 키의 데이터를 넣는 경우 업데이트가 반영되지 않아야 함.
        serializer = CommentCreateSerializer(
            comment_instance, data={"contnt": "updatedtestcontent"}, partial=True
        )
        assert serializer.is_valid()
        assert serializer.validated_data == {}


# 역시 retrieve, 즉 serialize가 제대로 되는지만 테스트한다.
class TestCommentRetrieveSerializer:
    @pytest.mark.django_db
    def test_model_serialization(self, comment_db_setup):
        comment_instance = comment_db_setup["comment_instance"]
        comment_db_setup["user_instance"].save()
        comment_db_setup["post_instance"].save()
        comment_db_setup["comment_instance"].save()
        comment_db_setup["file_instance"].save()

        serializer = CommentRetrieveSerializer(comment_instance)

        assert serializer.data["content"] == "testcontent"
        assert serializer.data["html_content"] == "html_testcontent"
        assert serializer.data["author"] == "KKKBBBSSS"
        assert serializer.data["files"][0]["file_location"] == "filelocation"
