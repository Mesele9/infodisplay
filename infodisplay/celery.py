
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'infodisplay.settings')

app = Celery('infodisplay')

app.config_from_object('django.conf:settings', namespace='CELERY', force=True)

#app.conf.broker_url = 'redis://localhost:6379/0'
#app.conf.result_backend = 'redis://localhost:6379/1'

app.conf.beat_schedule = {
    'fetch_time_60s': {
        'task': 'display.tasks.fetch_time_task',
        'schedule': 60.0,
    },
    'fetch_weather_600s': {
        'task': 'display.tasks.fetch_weather_task',
        'schedule': 600.0,
    },
     'daily_exchange_6h': {
        'task': 'display.tasks.daily_exchange_rate_task',
        'schedule': 21600.0,
    }
}

app.autodiscover_tasks()
