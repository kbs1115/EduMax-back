from rest_framework import status
from django.http import JsonResponse


def url_not_found(request, exception, *args, **kwargs):
    data = {"error": "URL not found (404)", "code": status.HTTP_404_NOT_FOUND}
    return JsonResponse(data, status=status.HTTP_404_NOT_FOUND)
