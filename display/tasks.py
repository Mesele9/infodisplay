import requests
from django.forms.models import model_to_dict
from datetime import datetime
import time
from bs4 import BeautifulSoup
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from celery import shared_task
from .models import City, CachedTime, CachedWeather, Currency, ExchangeRate


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
        time_url = "https://www.timeapi.io/api/Time/current/zone?timeZone={}/{}".format(timezone, city_name)

        response = requests.get(time_url)

        if response.status_code == 200:
            data = response.json()
            current_time_str = data['time']
            current_date_str = data['date']

            formated_current_time = datetime.strptime(current_time_str, "%H:%M").time()
            formated_current_date = datetime.strptime(current_date_str, "%m/%d/%Y").date()

            cached_time, created = CachedTime.objects.get_or_create(city=city['id'])
            cached_time.current_time = str(formated_current_time)
            cached_time.current_date = str(formated_current_date)
            cached_time.save()

            time_task_result.append({
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
    """A function to fetch weather from api"""
    cities_obj = get_cities()
    weather_task_result = []    
    for city in cities_obj:
        weather_api_start = time.time()
        city_name = city['name']

        api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&id=524901&appid=39dc2a00957e43bc26c6cbb435c7a8a1".format(city_name)
        
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            temperature = data['main']['temp']
            description = data['weather'][0]['description']
            icon = data['weather'][0]['icon']

            cached_weather, created = CachedWeather.objects.get_or_create(city=city['id'])
            cached_weather.temprature = temperature
            cached_weather.description = description
            cached_weather.icon = icon
            cached_weather.save()
            
            weather_task_result.append({
                'city': city_name,
                'temperature': cached_weather.temprature,
                'descritpion': cached_weather.description,
                'icon': cached_weather.icon
            })
        else:
            print("weather api failed")
    
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
    """ a function that scrap exchange rate from a url """

    url = "https://dashenbanksc.com/daily-exchange-rates/"
    res = requests.get(url)

    soup = BeautifulSoup(res.text, "html.parser")

    # get the applicable date
    date_element = soup.find("h4", style="text-align: center")
    if date_element:
        rate_applicable_date = date_element.get_text(strip=True)
    else:
        pass

    # get the exchange rate table data
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

    # get the currency names from the database
    currency_names = Currency.objects.values_list('name', flat=True)
    currency_to_display = {}
    for currency_name in currency_names:
        if currency_name in exchange_rate_data:
            currency_to_display[currency_name] = exchange_rate_data[currency_name]

            # save the scraped data to the ExchangeRAte model
            currency = Currency.objects.get(name=currency_name)
            ExchangeRate.objects.create(currency=currency, rate=exchange_rate_data[currency_name], applicable_date=rate_applicable_date)

    daily_exchange_data = {
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

