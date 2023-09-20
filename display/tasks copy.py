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
    """ a function that fetch the time fro api"""
    cities_obj = get_cities()
    time_task_result = []
    for city in cities_obj:
        time_api_starts = time.time()
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
            cached_time.current_time = formated_current_time
            cached_time.current_date = formated_current_date
            cached_time.save()
            
            time_api_end = time.time() - time_api_starts
            print(f"Time Api Time: {time_api_end}")
            print(f"{city_name}: time is {cached_time.current_time} and Date is {cached_time.current_date}")
            time_task_result.append({
                'city': city['name'],
                'current_time': cached_time.current_time,
                'current_date': cached_time.current_date
            })
        
        else:
            print("time api failed")
    
    print(f"time result after collected {time_task_result}")
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
            cached_weather.descritpion = description
            cached_weather.icon = icon
            cached_weather.save()


            weather_api_end = time.time() - weather_api_start
            print(f" Weather Api Time: {weather_api_end}")
            print(f"{city_name}: temp {cached_weather.temprature} {cached_weather.descritpion}")
            weather_task_result.append({
                'city': city_name,
                'temperature': cached_weather.temprature,
                'descritpion': cached_weather.descritpion,
                'icon': cached_weather.icon
            })
        else:
            print("weather api failed")
    print(f"weather task result{weather_task_result}")
    return weather_task_result


@shared_task
def daily_exchange_rate_task():
    """ a function that scrap exchange rate from a url """
    scrap_starts = time.time()

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
            ExchangeRate.objects.create(currency=currency, rate=exchange_rate_data[currency_name])

    print("{} {}".format(rate_applicable_date, currency_to_display))
    scrap_end = time.time() - scrap_starts
    print(f"Webscrap time: {scrap_end}")
    return {
        'rate_applicable_date': rate_applicable_date, 
        'currency_to_display': currency_to_display
    }

