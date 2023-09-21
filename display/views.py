from django.shortcuts import render
from django.http import HttpResponse
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import Rooms
from .tasks import fetch_time_task, fetch_weather_task, daily_exchange_rate_task


def merge_time_and_weather_data(time_data, weather_data):
    merged_data = []

    # Create a dictionary to map 'city' to its corresponding 'weather' data
    weather_data_map = {entry['city']: entry for entry in weather_data}

    for entry in time_data:
        city = entry['city']
        weather_entry = weather_data_map.get(city, {})
        merged_entry = {
            'city': city,
            'current_date': entry['current_date'],
            'current_time': entry['current_time'],
            'temperature': weather_entry.get('temperature', ''),
            'description': weather_entry.get('description', ''),
            'icon': weather_entry.get('icon', ''),
        }
        merged_data.append(merged_entry)

    return merged_data


def index(request):
    # Fetch data asynchronously without blocking the view
    time_task = fetch_time_task.delay()
    weather_task = fetch_weather_task.delay()
    exchange_rate_task = daily_exchange_rate_task.delay()

    # Wait for the results of the tasks
    time_data = time_task.get()
    weather_data = weather_task.get()
    exchange_rate_data = exchange_rate_task.get()

    # Merge time and weather data
    time_weather_data = merge_time_and_weather_data(time_data, weather_data)

    # Prepare the data to send to the frontend via WebSocket
    send_to_display = {
        'time_weather_data': time_weather_data,
        'exchange_rate_data': {
            'applicable_date': exchange_rate_data['rate_applicable_date'],
            'currency_to_display': exchange_rate_data['currency_to_display']
        }
    }

    # Send the data to the frontend via WebSocket
    channel_layer = get_channel_layer()
    
    channel_layer.group_send(
        'display',
        {
            'type': 'send_to_display',
            'data': send_to_display,
        }
    )

    # Render the HTML template
    context = {
        'time_weather_data': time_weather_data,
        'rate_applicable_date': exchange_rate_data['rate_applicable_date'],
        'currency_to_display': exchange_rate_data['currency_to_display'],
        'rooms': Rooms.objects.all(),  # Load rooms here, only when needed
    }

    return render(request, 'index.html', context)
