from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from community.service.file_service import FileService
from config.settings.base import AWS_S3_CUSTOM_DOMAIN


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def s3_uploader(request):
    if 'files' not in request.FILES:
        return Response(status=400,
                        data={
                            "message": "no files",
                            "data": None},
                        )

    file_service = FileService()
    files = request.FILES.getlist('files')

    files_path = []
    for file in files:
        path = file_service.make_file_path(file)
        file_service.s3_upload_file(file, path)
        full_path = f"https://{AWS_S3_CUSTOM_DOMAIN}/{path}"
        files_path.append(full_path)

    return Response(status=400,
                    data={
                        "message": "'Files uploaded successfully'",
                        "data": files_path}
                    )
