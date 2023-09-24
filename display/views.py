from django.shortcuts import render
from django.http import HttpResponse
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.cache import cache

from .models import Rooms, City
from .tasks import fetch_time_task, fetch_weather_task, daily_exchange_rate_task
from .utils import get_template_column_width, merge_time_and_weather_data


def index(request):
    # Fetch data asynchronously without blocking the view
    time_data = cache.get('fetch_time_task_result')
    weather_data = cache.get('fetch_weather_task_result')
    exchange_rate_data = cache.get('daily_exchange_rate_task_result')


    if time_data is None or weather_data is None or exchange_rate_data is None:
        # If any of the data is missing in the cache, fetch it using Celery tasks
        time_task = fetch_time_task.delay()
        weather_task = fetch_weather_task.delay()
        exchange_rate_task = daily_exchange_rate_task.delay()

        # Wait for the results
        time_data = time_task.get()
        weather_data = weather_task.get()
        exchange_rate_data = exchange_rate_task.get()

        # Store the results in cache
        cache.set('fetch_time_task_result', time_data, 60)
        cache.set('fetch_weather_task_result', weather_data, 600)
        cache.set('daily_exchange_rate_task_result', exchange_rate_data, 21000)


    time_weather_data = merge_time_and_weather_data(time_data, weather_data)

    # Render your template with the data
    context = {
        'time_weather_data': time_weather_data,
        'column_width': get_template_column_width(),
        'rate_applicable_date': exchange_rate_data['rate_applicable_date'],
        'currency_to_display': exchange_rate_data['currency_to_display'],
        'rooms': Rooms.objects.all(),
    }

    return render(request, 'index.html', context)
