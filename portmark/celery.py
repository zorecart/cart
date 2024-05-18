# portmark/celery.py
"""
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portmark.settings')

app = Celery('portmark')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'update-sold-fields': {
        'task': 'giftweb.tasks.update_sold_fields',
        'schedule': crontab(minute=0, hour='*/12'),  # Run every 12 hours
    },
}

app.conf.timezone = 'UTC'
"""