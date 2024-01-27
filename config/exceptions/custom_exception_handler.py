from rest_framework.views import exception_handler
from rest_framework import exceptions, status
from rest_framework.response import Response
from datetime import datetime
import logging


def custom_exception_handler(exc, context):
    logger = logging.getLogger("django")

    logger.error(f"[ERROR]")
    logger.error(f"[{datetime.now()}]")

    res = exception_handler(exc, context)

    if res is not None:
        if isinstance(exc, exceptions.APIException):
            logger.error(f"> exception")
            logger.error(f"{exc}")
            logger.error(f"> context")
            logger.error(f"{context}")

            errors = exc.detail
        else:
            errors = "unknown error"

        return Response(
            {
                "code": res.status_code,
                "errors": errors,
            },
            status=res.status_code,
        )
