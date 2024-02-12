import pytest

from community.model.access import *
from community.domain.definition import (
    LectureCategoriesDepth1Param,
)


class TestLectureAccessFunctions:
    @pytest.mark.django_db
    def test_get_lectures_with_category(self, user_instance, lecture_db_setup):
        user_instance.save()
        lecture_db_setup["lecture_instances"][0].save()
        lecture_db_setup["lecture_instances"][1].save()
        
        eng_lectures = get_lectures_with_category(LectureCategoriesDepth1Param.ENGLISH)
        korean_lectures = get_lectures_with_category(LectureCategoriesDepth1Param.KOREAN)
        math_lectures = get_lectures_with_category(LectureCategoriesDepth1Param.MATH)
        
        assert len(eng_lectures) == 1
        assert len(korean_lectures) == 1
        assert len(math_lectures) == 0
            
        with pytest.raises(TypeError):
            korean_lectures = get_lectures_with_category("KOR")
    
    @pytest.mark.django_db
    def test_get_lecture_from_id(self, lecture_db_setup):
        lecture_db_setup["user_instance"].save()
        lecture_db_setup["lecture_instances"][0].save()
        
        lecture = get_lecture_from_id(lecture_db_setup["lecture_instances"][0].id)
        
        assert lecture.title == lecture_db_setup["lecture_instances"][0].title
        
        with pytest.raises(NotFound):
            lecture = get_lecture_from_id(2)
            
    
    @pytest.mark.django_db
    def test_get_lecture_from_id(self, lecture_db_setup):
        lecture_db_setup["user_instance"].save()
        lecture_db_setup["lecture_instances"][0].save()
        
        lecture_author = get_lecture_user_id(lecture_db_setup["lecture_instances"][0].id)
        author = User.objects.get(id=lecture_author)
        assert author.nickname == lecture_db_setup["user_instance"].nickname
        
        lecture_db_setup["user_instance"].delete()
        with pytest.raises(NotFound):
            lecture_author = get_lecture_user_id(lecture_db_setup["lecture_instances"][0].id)
            