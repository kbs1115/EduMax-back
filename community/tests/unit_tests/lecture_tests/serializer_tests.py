import pytest

from community.serializers import LectureListSerializer, LectureRetrieveSerializer, LectureCreateSerializer
from community.domain.validation import CategoryValidator


class TestLectureListSerializer:
    @pytest.mark.django_db
    def test_model_serialization(self, lecture_db_setup):
        lecture_instances = lecture_db_setup["lecture_instances"]
        lecture_db_setup["user_instance"].save()
        lecture_db_setup["lecture_instances"][0].save()
        lecture_db_setup["lecture_instances"][1].save()

        serializer = LectureListSerializer(lecture_instances, many=True)

        assert len(serializer.data) == 2
        assert serializer.data[0]["title"] == lecture_instances[0].title


class TestLectureRetrieveSerializer:
    @pytest.mark.django_db
    def test_model_serialization(self, lecture_db_setup):
        lecture_instance = lecture_db_setup["lecture_instances"][0]
        lecture_db_setup["user_instance"].save()
        lecture_instance.save()

        serializer = LectureRetrieveSerializer(lecture_instance)

        assert serializer.data["title"] == lecture_instance.title
        assert serializer.data["category_d2"] == None
        assert serializer.data["author"] == lecture_instance.author.nickname


class TestLectureCreateSerializer:
    @pytest.mark.django_db
    def test_model_deserialization(self, valid_serialized_lecture_data, lecture_instances, user_instance, mocker):
        mocker.patch.object(CategoryValidator, "validate")
        user_instance.save()

        serializer = LectureCreateSerializer(data=valid_serialized_lecture_data)
        assert serializer.is_valid()
        assert serializer.errors == {}

        serializer = LectureCreateSerializer(
            lecture_instances[0], data={"title": "newtesttitle"}, partial=True
        )

        assert serializer.is_valid()
        assert serializer.errors == {}
        assert serializer.validated_data == {"title": "newtesttitle"}

    @pytest.mark.django_db
    def test_invalid_model_deserialization(self, invalid_serialized_lecture_data, lecture_instances, user_instance,
                                           mocker):
        mocker.patch.object(CategoryValidator, "validate")
        user_instance.save()

        # youtube_title이 없을 때 test
        serializer = LectureCreateSerializer(data=invalid_serialized_lecture_data)
        assert not serializer.is_valid()

        # 존재하지 않는 author를 설정할 때 test
        serializer = LectureCreateSerializer(
            lecture_instances[0], data={"author": 3}, partial=True
        )

        assert not serializer.is_valid()
        assert serializer.validated_data == {}
