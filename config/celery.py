import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Create the Celery app with a name that reflects your project.
app = Celery('data-platform')

# Load Celery configuration from Django settings (using the CELERY namespace).
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically discover tasks in all apps listed in INSTALLED_APPS.
app.autodiscover_tasks()

# Optional: Debug task for troubleshooting.
@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')