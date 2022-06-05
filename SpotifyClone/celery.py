import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SpotifyClone.settings')
app = Celery('SpotifyClone')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
