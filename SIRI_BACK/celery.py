import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SIRI_BACK.settings")
app = Celery("SIRI_CELERY_APP")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
