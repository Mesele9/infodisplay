import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'infodisplay.settings')

app = Celery('infodisplay')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'fetch_time_60s': {
        'task': 'display.tasks.fetch_time_task',
        'schedule': 60.0,
    },
    'fetch_weather_120s': {
        'task': 'display.tasks.fetch_weather_task',
        'schedule': 120.0,
    },
     'daily_exchange_120s': {
        'task': 'display.tasks.daily_exchange_rate_task',
        'schedule': 120.0,
    }
}

app.autodiscover_tasks()