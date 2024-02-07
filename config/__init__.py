# path/to/your/proj/__init__.py
# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from config.celery_file import app as celery_app  # noqa

__all__ = ('celery_app',)
