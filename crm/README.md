# CRM Celery + Redis Setup

This guide explains how to set up **Celery** with **Redis** and **Celery Beat** for scheduled tasks in the CRM project.  
It covers installation, configuration, running services, and verifying logs.

---

## 1. Install Dependencies

### 1.1 System Requirements
- Python 3.8+
- Redis (must be installed and running locally)
- A working Django project named **crm**

### 1.2 Install Python Packages
Add to `requirements.txt`:

celery
django-celery-beat
requests


Then install:

```bash
pip install -r requirements.txt

2. Start Redis

If Redis is installed locally:

redis-server

Check it is running:

redis-cli ping

Expected output:

PONG

3. Configure Django for Celery
3.1 Update crm/settings.py

Add to INSTALLED_APPS:

INSTALLED_APPS = [
    # default Django apps...
    "django_celery_beat",
    "crm",
]

Add Celery + Beat configuration:

from celery.schedules import crontab

CELERY_BROKER_URL = "redis://localhost:6379/0"

CELERY_BEAT_SCHEDULE = {
    "generate-crm-report": {
        "task": "crm.tasks.generate_crm_report",
        "schedule": crontab(day_of_week="mon", hour=6, minute=0),
    },
}

3.2 Create crm/celery.py

import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crm.settings")

app = Celery("crm")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

3.3 Update crm/__init__.py

from .celery import app as celery_app

__all__ = ("celery_app",)

4. Database Setup

Run migrations for Django and Celery Beat:

python manage.py migrate
python manage.py migrate django_celery_beat

5. Define Celery Task

Create crm/tasks.py:

import requests
from datetime import datetime
from celery import shared_task

@shared_task
def generate_crm_report():
    log_file = "/tmp/crm_report_log.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    query = """
    query {
        customers {
            id
        }
        orders {
            id
            totalAmount
        }
    }
    """

    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": query},
            timeout=10
        )
        data = response.json().get("data", {})

        customers = data.get("customers", [])
        orders = data.get("orders", [])

        total_customers = len(customers)
        total_orders = len(orders)
        total_revenue = sum(float(o.get("totalAmount", 0)) for o in orders)

        message = f"{timestamp} - Report: {total_customers} customers, {total_orders} orders, {total_revenue} revenue"

        with open(log_file, "a") as f:
            f.write(message + "\n")

    except Exception as e:
        with open(log_file, "a") as f:
            f.write(f"{timestamp} - Error generating report: {e}\n")

6. Run Celery

You need two processes:

    Celery worker (to process tasks)

    Celery Beat (to schedule tasks)

6.1 Start Celery Worker

celery -A crm worker -l info

6.2 Start Celery Beat

In a second terminal:

celery -A crm beat -l info

7. Verify Scheduled Reports

The scheduled task runs every Monday at 6:00 AM.
It appends a line to:

/tmp/crm_report_log.txt

Example:

2025-09-01 06:00:00 - Report: 120 customers, 350 orders, 24500.0 revenue

If an error occurs, it will also be logged in the same file.
8. Manual Testing

You can trigger the task manually:

python manage.py shell

from crm.tasks import generate_crm_report
generate_crm_report.delay()

This will enqueue the report task immediately.
Check /tmp/crm_report_log.txt to verify it worked.