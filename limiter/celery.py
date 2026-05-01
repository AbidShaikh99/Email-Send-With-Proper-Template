import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'limiter.settings')

app = Celery('limiter')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()