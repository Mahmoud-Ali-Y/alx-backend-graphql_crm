import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crm.settings")

app = Celery("crm")

# Load settings from Django settings file, namespace 'CELERY'
app.config_from_object("django.conf:settings", namespace="CELERY")

# Discover tasks from all installed apps
app.autodiscover_tasks()