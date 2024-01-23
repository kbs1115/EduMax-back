import uuid

from botocore.exceptions import ClientError
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from community.models import Post, Comment, File
from community.serializers import FileSerializer


class FileService:
    # file을 올리기전에 여러 validation이 필요할것으로 예상되지만 일단 pass

    def upload_file(self, file, path):
        try:
            default_storage.save(path, ContentFile(file.read()))  # 장고에서 모든 request.Files는 contentFile instance에 속함
        except ClientError as e:
            raise e
        except Exception as e:
            raise e

    def make_files_path(self, file):
        # s3 에서 해당 파일의 id 역할을 한다.
        unique_id = str(uuid.uuid4())
        file_path = f"media/{unique_id}_{file.name}"
        return file_path

    def make_dict_for_serialize(self, file_path, related_model_instance):
        if isinstance(related_model_instance, Post):
            post = related_model_instance
            return {
                "post": post.id,
                "file_location": file_path
            }
        if isinstance(related_model_instance, Comment):
            pass

    def create_files(self, request, related_model_instance):

        try:
            files = request.FILES.getlist('files')
        except Exception as e:
            return e
        try:
            for file in files:
                f_path = self.make_files_path(file)
                self.upload_file(file, f_path)

                dict_data = self.make_dict_for_serialize(f_path, related_model_instance)
                serializer = FileSerializer(data=dict_data)
                if not serializer.is_valid():
                    raise serializer.errors
                serializer.save()
        except ClientError as e:
            return e
        except Exception as e:
            return e

    # files을 삭제한다.
    def delete_files(self, related_model_instance):
        try:
            files_id = File.objects.filter(post=related_model_instance).values_list('id', flat=True)
            for file_id in files_id:
                instance = File.objects.get(pk=file_id)
                file_path = instance.file_location
                default_storage.delete(file_path)
                instance.delete()
        except File.DoesNotExist as e:
            return e
        except ClientError as e:
            return e
        except Exception as e:
            return e

    def put_files(self, request, related_model_instance):
        files_state = request.data.get('files_state', None)
        try:
            if files_state == 'replace':
                self.delete_files(related_model_instance)
                self.create_files(request, related_model_instance)
            if files_state == 'delete':
                self.delete_files(related_model_instance)
        except Exception as e:
            return e

    # 하나의 file path를 요구할때 ->아직 필요x
    def retrieve_file(self):
        pass

    # file path들을 돌려준다. ->아직 필요x
    def list_file(self):
        pass

    # 서버에서 직접 다운로드 할때 ->아직 필요x
    def download_files(self, paths):
        # front 에서 file path 만 주고 직접 다운로드 할수 있게 한다.
        pass
