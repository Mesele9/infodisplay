import requests
from .models import CachedTime, City
from datetime import datetime, date, time
import time


def fetch_time(city):
    """ a function that fetch the time fro api"""
    time_api_starts = time.time()
    timezone = city.city_timezone
    city_name = city.name
    time_url = "https://www.timeapi.io/api/Time/current/zone?timeZone={}/{}".format(timezone, city_name)

    response = requests.get(time_url)

    if response.status_code == 200:
        data = response.json()
        current_time_str = data['time']
        current_date_str = data['date']

        formated_current_time = datetime.strptime(current_time_str, "%H:%M").time()
        formated_current_date = datetime.strptime(current_date_str, "%m/%d/%Y").date()

        cached_time, created = CachedTime.objects.get_or_create(city=city)
        cached_time.current_time = formated_current_time
        cached_time.current_date = formated_current_date
        cached_time.save()
        
        time_api_end = time.time() - time_api_starts
        print(f"Time Api Time: {time_api_end}")
        print(f"{city_name}: time is {cached_time.current_time} and Dateis {cached_time.current_date}")
        return cached_time
    else:
        print("time api failed")