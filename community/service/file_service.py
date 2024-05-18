import uuid
import magic

from botocore.exceptions import ClientError
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import transaction
from rest_framework import exceptions

from community.model.models import Post, Comment, File
from community.serializers import FileSerializer


class FileService:
    @classmethod
    def is_valid_file_extension(cls, file_name, allowed_extensions):
        extension = file_name.rsplit('.', 1)[1].lower()
        return extension in allowed_extensions

    @classmethod
    def s3_upload_file(cls, file, path):
        # 파일 MIME 타입 검사
        mime = magic.Magic(mime=True)
        file_mime_type = mime.from_buffer(file.read(1024))  # 파일 시작 부분의 데이터로 MIME 타입 결정
        file.seek(0)  # 파일 읽기 위치를 다시 시작점으로 이동

        # 허용하는 MIME 타입 리스트 수정
        allowed_mime_types = [
            'audio/', 'image/', 'video/',
            'application/pdf',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/vnd.hancom.hwp',
            'application/vnd.ms-powerpoint',
            'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            'application/zip'  # ZIP 포맷 추가
        ]

        # 확장자 기반 허용 목록
        allowed_extensions = {
            'jpg', 'jpeg', 'png', 'gif',
            'mp3', 'wav',
            'mp4', 'avi',
            'pdf',
            'doc', 'docx',
            'ppt', 'pptx',
            'hwp'
        }

        # 파일 타입 확인 (MIME 타입과 확장자 검사)
        if any(file_mime_type.startswith(allowed_type) for allowed_type in
               allowed_mime_types) and cls.is_valid_file_extension(file.name, allowed_extensions):
            # 파일 크기 확인
            file.seek(0, 2)  # 파일의 끝으로 이동
            file_size = file.tell()  # 파일 크기를 바이트 단위로 얻음
            file.seek(0)  # 파일 읽기 위치를 다시 시작점으로 이동

            # 20MB = 20 * 1024 * 1024 바이트
            if file_size <= 20 * 1024 * 1024:
                try:
                    default_storage.save(
                        path, ContentFile(file.read())
                    )
                except ClientError:
                    raise ClientError
            else:
                raise ValueError("File size exceeds the maximum limit of 20MB.")
        else:
            raise ValueError("Unsupported file type.")

    @classmethod
    def s3_delete_file(cls, file_path):
        try:
            default_storage.delete(file_path)
        except ClientError:
            raise ClientError

    @classmethod
    def make_file_path(cls, file):
        # s3 에서 해당 파일의 id 역할을 한다.
        unique_id = str(uuid.uuid4())
        file_path = f"media/{unique_id}_{file.name}"
        return file_path

    @classmethod
    def make_dict_for_serialize(cls, file_path, related_model_instance, file_name):
        # file 시리얼라이저을 위한 딕셔너리 만들기
        if isinstance(related_model_instance, Post):
            post = related_model_instance
            return {"post": post.id, "file_location": file_path, "name": file_name}
        if isinstance(related_model_instance, Comment):
            comment = related_model_instance
            return {"comment": comment.id, "file_location": file_path, "name": file_name}

    @classmethod
    def get_files_id_list(cls, related_model_instance):
        if isinstance(related_model_instance, Post):
            return File.objects.filter(post=related_model_instance).values_list(
                "id", flat=True
            )
        if isinstance(related_model_instance, Comment):
            return File.objects.filter(comment=related_model_instance).values_list(
                "id", flat=True
            )

    @classmethod
    def get_file_instance(cls, file_id):
        try:
            return File.objects.get(pk=file_id)
        except File.DoesNotExist:
            raise exceptions.NotFound("file not found")

    def create_files(self, files, related_model_instance):
        # files s3저장, file model 저장

        for file in files:
            f_path = self.make_file_path(file)
            dict_data = self.make_dict_for_serialize(f_path, related_model_instance, file.name)
            serializer = FileSerializer(data=dict_data)
            if not serializer.is_valid():
                print(serializer.errors)
                raise exceptions.ValidationError(serializer.errors)

            with transaction.atomic():
                serializer.save()

                # If s3_upload_file에서 에러발생하면 롤백
                self.s3_upload_file(file, f_path)

    def delete_files(self, related_model_instance):
        # files 삭제- s3삭제, file model 삭제

        files_id = self.get_files_id_list(related_model_instance)
        for file_id in files_id:
            instance = self.get_file_instance(file_id)
            file_path = instance.file_location
            with transaction.atomic():
                instance.delete()

                # If s3_delete_file에서 에러발생하면 롤백
                self.s3_delete_file(file_path)

    def put_files(self, files, related_model_instance):
        # file 수정 - put 방식을 사용, 기존꺼 삭제, 새로운거 생성
        self.delete_files(related_model_instance)
        self.create_files(files, related_model_instance)

    # 서버에서 직접 다운로드 할때 ->아직 필요x
    def download_files(self, paths):
        # front 에서 file path 만 주고 직접 다운로드 할수 있게 한다.
        pass
