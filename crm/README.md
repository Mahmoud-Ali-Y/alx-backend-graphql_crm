# CRM Celery Setup

## Prerequisites
- Install Redis
- Install requirements:
  ```bash
  pip install -r requirements.txt
  python manage.py migrate
  celery -A crm worker -l info
  celery -A crm beat -l info
  Check generated reports in:
  /tmp/crm_report_log.txt