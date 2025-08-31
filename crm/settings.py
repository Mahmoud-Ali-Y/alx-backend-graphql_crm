from celery.schedules import crontab

CELERY_BROKER_URL = "redis://localhost:6379/0"

CELERY_BEAT_SCHEDULE = {
    "generate-crm-report": {
        "task": "crm.tasks.generate_crm_report",
        "schedule": crontab(day_of_week="mon", hour=6, minute=0),
    },
}

INSTALLED_APPS = [
    # default apps...
    "django.contrib.staticfiles",
    "django_crontab",
    "properties",  # if still present
    "crm",         # ensure crm is listed
    "django_celery_beat",
]

CRONJOBS = [
    # Run every 5 minutes for testing (adjust schedule as needed)
    ("*/5 * * * *", "crm.cron.log_crm_heartbeat"),
]
CRONJOBS = [
    ("0 3 * * *", "crm.cron.update_low_stock"),  # run daily at 3:00 AM
]