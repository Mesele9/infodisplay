import requests
from celery import shared_task
from .models import City

from .timeapi import fetch_time
from .weatherapi import fetch_weather
from .scrap import daily_exchange_rate


@shared_task
def fetch_time_task():
    cities = City.objects.all()
    return [fetch_time(city) for city in cities]
    """for city in cities:
        fetch_time(city)"""
    return aggregated_fetch_city_time

@shared_task
def fetch_weather_task():
    cities = City.objects.all()
    return [fetch_weather(city) for city in cities]
    """for city in cities:
        fetch_weather(city)"""
    return aggregated_fetch_city_weather


@shared_task
def daily_exchange_rate_task():
    return daily_exchange_rate()