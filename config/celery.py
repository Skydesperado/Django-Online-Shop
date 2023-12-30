import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.hostname = settings.CELERY_HOST_NAME


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
