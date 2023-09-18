import requests
from .models import City, CachedWeather
import time

def fetch_weather(city):
    """A function to fetch weather from api"""
    weather_api_start = time.time()
    city_name = city.name

    api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&id=524901&appid=39dc2a00957e43bc26c6cbb435c7a8a1".format(city_name)
    
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']

        cached_weather, created = CachedWeather.objects.get_or_create(city=city)
        cached_weather.temprature = temperature
        cached_weather.descritpion = description
        cached_weather.icon = icon
        cached_weather.save()


        weather_api_end = time.time() - weather_api_start
        print(f" Weather Api Time: {weather_api_end}")
        print(f"{city_name}: temp {cached_weather.temprature} {cached_weather.descritpion}")
        return cached_weather
    else:
        print("weather api failed")
