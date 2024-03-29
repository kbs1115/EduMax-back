import uuid

from botocore.exceptions import ClientError
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import transaction
from rest_framework import exceptions

from community.model.models import Post, Comment, File
from community.serializers import FileSerializer


class FileService:
    # file을 올리기전에 여러 validation이 필요할것으로 예상되지만 일단 pass
    @classmethod
    def s3_upload_file(cls, file, path):
        # s3에 파일을 업로드한다
        try:
            default_storage.save(
                path, ContentFile(file.read())
            )  # 장고에서 모든 request.Files는 contentFile instance에 속함
        except ClientError:
            raise ClientError

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
    def make_dict_for_serialize(cls, file_path, related_model_instance):
        # file 시리얼라이저을 위한 딕셔너리 만들기
        if isinstance(related_model_instance, Post):
            post = related_model_instance
            return {"post": post.id, "file_location": file_path}
        if isinstance(related_model_instance, Comment):
            comment = related_model_instance
            return {"comment": comment.id, "file_location": file_path}

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
            dict_data = self.make_dict_for_serialize(f_path, related_model_instance)
            serializer = FileSerializer(data=dict_data)
            if not serializer.is_valid():
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
