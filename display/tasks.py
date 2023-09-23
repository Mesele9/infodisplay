import requests
from django.forms.models import model_to_dict
from datetime import datetime
import time
from bs4 import BeautifulSoup
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from celery import shared_task
from .models import City, CachedTime, CachedWeather, Currency, ExchangeRate
from decouple import config

api_key = config('OPENWEATHERMAP_API_KEY', default='')

channel_layer = get_channel_layer()

def get_cities():
    cities = City.objects.all()
    cities_obj = [model_to_dict(city) for city in cities]
    return cities_obj

@shared_task
def fetch_time_task():
    """A function that fetches the time from an API, saves it to the database, and sends it to the WebSocket."""
    cities_obj = get_cities()
    time_task_result = []

    for city in cities_obj:
        timezone = city['city_timezone']
        city_name = city['name']
        time_url = f"https://www.timeapi.io/api/Time/current/zone?timeZone={timezone}/{city_name}"

        response = requests.get(time_url)

        if response.status_code == 200:
            data = response.json()
            current_time_str = data['time']
            current_date_str = data['date']

            formated_current_time = datetime.strptime(current_time_str, "%H:%M").time()
            formated_current_date = datetime.strptime(current_date_str, "%m/%d/%Y").date()

            city_instance = City.objects.get(id=city['id'])
            print(city_instance)
                                            
            cached_time, created = CachedTime.objects.get_or_create(city=city_instance)
            cached_time.current_time = str(formated_current_time)
            cached_time.current_date = str(formated_current_date)
            cached_time.save()

            time_task_result.append({
                'source': 'time',
                'city': city['name'],
                'current_time': cached_time.current_time,
                'current_date': cached_time.current_date
            })

    # Send the data to the WebSocket group
    async_to_sync(channel_layer.group_send)(
        'display',
        {
            'type': 'send_to_display',
            'data': time_task_result,
        }
    )

    print(time_task_result)

    return time_task_result

@shared_task
def fetch_weather_task():
    """A function to fetch weather from an API"""
    cities_obj = get_cities()
    weather_task_result = []    
    for city in cities_obj:
        city_name = city['name']

        api_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&id=524901&appid={api_key}"
        
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            temperature = data['main']['temp']
            description = data['weather'][0]['description']
            icon = data['weather'][0]['icon']

            city_instance = City.objects.get(id=city['id'])
            print(city_instance)

            cached_weather, created = CachedWeather.objects.get_or_create(city=city_instance)
            cached_weather.temperature = temperature
            cached_weather.description = description
            cached_weather.icon = icon
            cached_weather.save()
            
            weather_task_result.append({
                'source': 'weather',
                'city': city_name,
                'temperature': cached_weather.temperature,
                'description': cached_weather.description,
                'icon': cached_weather.icon
            })
        else:
            print("Weather API failed")
    
    # Send the data to the WebSocket group
    async_to_sync(channel_layer.group_send)(
        'display',
        {
            'type': 'send_to_display',
            'data': weather_task_result,
        }
    )

    return weather_task_result

@shared_task
def daily_exchange_rate_task():
    """A function that scrapes exchange rates from a website"""
    url = "https://dashenbanksc.com/daily-exchange-rates/"
    res = requests.get(url)

    soup = BeautifulSoup(res.text, "html.parser")

    # Get the applicable date
    date_element = soup.find("h4", style="text-align: center")
    if date_element:
        rate_applicable_date = date_element.get_text(strip=True)
    else:
        pass

    # Get the exchange rate table data
    item = soup.find('table')
    if item:
        exchange_rate_data = {}
        for row in item.find_all('tr')[1:]:
            columns = row.find_all('td')
            currency = columns[1].get_text(strip=True)
            rate = columns[2].get_text(strip=True)

            exchange_rate_data[currency] = rate
        
    else:
        pass

    # Get the currency names from the database
    currency_names = Currency.objects.values_list('name', flat=True)
    currency_to_display = {}
    for currency_name in currency_names:
        if currency_name in exchange_rate_data:
            currency_to_display[currency_name] = exchange_rate_data[currency_name]

            # Save the scraped data to the ExchangeRate model
            currency = Currency.objects.get(name=currency_name)
            ExchangeRate.objects.create(currency=currency, rate=exchange_rate_data[currency_name], applicable_date=rate_applicable_date)

    daily_exchange_data = {
        'source': 'exchange',
        'rate_applicable_date': rate_applicable_date, 
        'currency_to_display': currency_to_display
    }
    
    # Send the data to the WebSocket group
    async_to_sync(channel_layer.group_send)(
        'display',
        {
            'type': 'send_to_display',
            'data': daily_exchange_data,
        }
    )

    return daily_exchange_data
