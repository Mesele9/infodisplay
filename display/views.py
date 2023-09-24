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

    # Check if the cached data is missing or expired for each data type
    if time_data is None:
        time_task = fetch_time_task.delay()
        time_data = time_task.get()

    if weather_data is None:
        weather_task = fetch_weather_task.delay()
        weather_data = weather_task.get()

    if exchange_rate_data is None:
        exchange_rate_task = daily_exchange_rate_task.delay()
        exchange_rate_data = exchange_rate_task.get()


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
