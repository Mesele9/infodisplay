from django.shortcuts import render
from django.http import HttpResponse
import json
from django.forms.models import model_to_dict
from asgiref.sync import async_to_sync
from  channels.layers import get_channel_layer

from .models import City, Rooms
from .tasks import fetch_time_task, fetch_weather_task, daily_exchange_rate_task


def index(request):
    
    rooms = Rooms.objects.all()

    # Fetch weather and time data for all cities asynchronously using Celery
    cities = City.objects.all()

    results = []

    channel_layer = get_channel_layer()

    for city in cities:
        time_task = fetch_time_task.delay()
        time_data = time_task.get()

        weather_task = fetch_weather_task.delay()
        weather_data = weather_task.get()

        results.append({
            'city': city,
            'time_data': time_data,
            'weather_data': weather_data
        })
    print(f"inside the view fucntion {results}")

    exchange_rate_task = daily_exchange_rate_task.delay()
    rate_applicable_date, currency_to_display = exchange_rate_task.get()

    
    # Prepare the data to send to the frontend via WebSocket
    data_to_send = {
        'time_weather_data': results,
        'exchange_rate_data': {
            'applicable_date': rate_applicable_date,
            'currency_to_display': currency_to_display
        }
    }

    # Send the data to the frontend via WebSocket
    async_to_sync(channel_layer.group_send)(
        'display',
        {
            'type': 'send_to_display',
            'data': data_to_send
        }
    )

    # Render the HTML template
    context = {
        'cities_data': results,
        'applicable_date': rate_applicable_date,
        'currency_to_display': currency_to_display,
        'rooms': rooms,
    }

    return render(request, 'index.html', context)

