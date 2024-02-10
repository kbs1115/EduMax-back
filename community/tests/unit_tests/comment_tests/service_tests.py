import pytest
from unittest.mock import Mock

from community.model.models import Post, Comment
from .conftests import *
from community.service.comment_service import *
from community.domain.definition import PostFilesState


class TestCommentService:
    def test_get_comment(self, mocker, comment_instance):
        # 1. Comment.objects.get 모킹
        mocked_get = mocker.patch.object(Comment.objects, "get")
        mocked_get.return_value = comment_instance

        # 2. CommentRetrieveSerializer 모킹
        mocked_serializer_instance = Mock(data={"test": "success"})
        mocker.patch(
            "community.service.comment_service.CommentRetrieveSerializer",
            return_value=mocked_serializer_instance,
        )

        # 3. CommentService.get_comment 호출
        res = CommentService.get_comment(1)

        # 4. 결과 검증
        assert res["status"] == 200
        assert res["message"] == "Comment retrieve successfully"
        assert res["data"] == {"test": "success"}

        # 5. 오류 발생 가정
        mocked_get.side_effect = Comment.DoesNotExist

        # 6. 예외 처리 확인
        with pytest.raises(NotFound):
            res = CommentService.get_comment(2)

    # 일단 file이 없는 상황만 테스트(뭘 넣어줄 지 잘모르겠다.)
    def test_create_comment(
        self,
        mocker,
        user_instance,
        comment_instance,
        mocked_get_parent_post_id,
        mocked_get_post_from_id,
        mocked_create_files,
        mocked_comment_create_serializer,
    ):
        # 1. input data 생성
        mock_files = [Mock(), Mock()]
        body = {
            "content": "contenttest1",
            "html_content": "htmlcontenttest1",
            "files": mock_files,
            "author": user_instance,
            "parent_comment_id": 1,
            "post_id": None,
        }

        # 2. 함수 mocking
        mocker.patch.object(transaction, "atomic")
        mocked_comment_create_serializer.save.return_value = comment_instance

        # 3. 함수 실행
        res = CommentService.create_comment(**body)

        # 4. 함수 호출 및 output 데이터 검증
        mocked_get_parent_post_id.assert_called_once()
        mocked_get_post_from_id.assert_called_once()
        mocked_comment_create_serializer.save.assert_called_once()
        mocked_create_files.assert_called_once()

        assert res["message"] == "Comment created successfully"
        assert res["status_code"] == 201
        assert res["data"] == {
            "id": 1,
            "post_id": 1,
            "author": "kbs1115",
        }

        # 5. serializer is_valid error 상황
        mocked_comment_create_serializer.is_valid.return_value = False

        # 6. 예외 처리 확인
        with pytest.raises(ValidationError):
            res = CommentService.create_comment(**body)

    # 일단 file이 없는 상황만 테스트(뭘 넣어줄 지 잘모르겠다.)
    def test_update_comment(
        self,
        mocker,
        comment_instance,
        mocked_get_comment_from_id,
        mocked_comment_create_serializer,
        mocked_put_files,
        mocked_delete_files,
    ):
        # 1. 함수에 넣을 데이터 생성
        mock_files = [Mock(), Mock()]
        body = [
            {
                "content": "updatecontent",
                "html_content": "updatehtmlcontent",
                "files": mock_files,
                "files_state": PostFilesState.DELETE,
            },
            {
                "content": "updatecontent",
                "html_content": "updatehtmlcontent",
                "files": mock_files,
                "files_state": PostFilesState.REPLACE,
            },
        ]

        # 2. 함수 mocking
        mocker.patch.object(transaction, "atomic")
        mocked_comment_create_serializer.save.return_value = comment_instance

        for i, instance in enumerate(body):
            # 3. 함수 실행(case 0)
            res = CommentService.update_comment(1, **instance)

            # 4. 함수 호출 및 output 데이터 검증
            assert mocked_get_comment_from_id.call_count == i + 1
            assert mocked_comment_create_serializer.save.call_count == i + 1
            if i == 0:
                mocked_delete_files.assert_called_once()
            elif i == 1:
                mocked_put_files.assert_called_once()

            assert res["message"] == "Comment updated successfully"
            assert res["status_code"] == 200
            assert res["data"] == {
                "id": 1,
                "post_id": 1,
                "author": "kbs1115",
            }

        # 5. serializer is_valid error 상황
        mocked_comment_create_serializer.is_valid.return_value = False

        # 6. 예외 처리 확인
        with pytest.raises(ValidationError):
            res = CommentService.update_comment(1, **body[0])

        # 7. FileState 오류 메시지 확인
        mocked_comment_create_serializer.is_valid.return_value = True
        body = {
            "content": "updatecontent",
            "html_content": "updatehtmlcontent",
            "files": None,
            "files_state": PostFilesState.REPLACE,
        }

        res = CommentService.update_comment(1, **body)

        assert res["message"] == "files_state is wrong"
        assert res["status_code"] == 400

    def test_delete_comment(
        self, mocker, mocked_get_comment_from_id, mocked_delete_files
    ):
        # 1. 함수 mocking
        mocker.patch.object(transaction, "atomic")
        mocked_delete = mocker.patch.object(Comment, "delete")

        # 2. 함수 호출 및 검증
        res = CommentService.delete_comment(1)

        mocked_get_comment_from_id.assert_called_once()
        mocked_delete_files.assert_called_once()
        mocked_delete.assert_called_once()

        assert res["message"] == "Comment deleted successfully"
        assert res["status_code"] == 204
