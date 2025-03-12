import os
from celery import Celery

# Set environment variable for Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weather_dashboard.settings")

celery_app = Celery("weather_dashboard")

# Load Celery settings from Django settings
celery_app.config_from_object("django.conf:settings", namespace="CELERY")

# Automatically discover tasks from installed Django apps
celery_app.autodiscover_tasks()

@celery_app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
