import os
from .celery import app as celery_app

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SIRI_BACK.settings')
__all__ = ['celery_app']
