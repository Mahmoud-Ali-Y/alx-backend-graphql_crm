INSTALLED_APPS = [
    # default apps...
    "django.contrib.staticfiles",
    "django_crontab",
    "properties",  # if still present
    "crm",         # ensure crm is listed
]

CRONJOBS = [
    # Run every 5 minutes for testing (adjust schedule as needed)
    ("*/5 * * * *", "crm.cron.log_crm_heartbeat"),
]