import os

from celery import Celery
from celery.schedules import crontab


import django

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()
from api.models import Upvote

app = Celery("core")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Executes every 10 second
    sender.add_periodic_task(10.0, delete_upvote.s(), name='delete every 10')
    
    # Executes everyday at 10:30 a.m.
    sender.add_periodic_task(
        crontab(hour=10, minute=30, day_of_week="*"),
        delete_upvote.s(),
    )


@app.task
def delete_upvote():
    Upvote.objects.all().delete()
    print("Upvotes deleted")


# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
