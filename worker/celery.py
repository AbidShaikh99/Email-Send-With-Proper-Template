import celery
from celery import Celery
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'limiter.settings')
app = celery.Celery(
    'worker',
    broker = 'redis://localhost:6379/0',
    backend = 'redis://localhost:6379/0',
    include = ['worker.tasks']
)
