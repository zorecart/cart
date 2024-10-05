# giftweb/tasks.py
"""
from celery import Celery
from django.apps import apps
from django.utils import timezone
import random

app = Celery('portmark')

@app.task
def update_sold_fields():
    Document = apps.get_model('giftweb', 'Document')
    documents = Document.objects.all()

    for document in documents:
        document.update_sold_field()
"""