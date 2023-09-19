from django.shortcuts import render
from django.http import HttpResponse
from django.forms.models import model_to_dict

from .models import City, Rooms, ExchangeRate
#from .timeapi import fetch_time
from .tasks import fetch_time_task, fetch_weather_task, daily_exchange_rate_task
"""from .weatherapi import fetch_weather
from .timeapi import fetch_time
from .scrap import daily_exchange_rate
"""


def index(request):
    
    rooms = Rooms.objects.all()

    """ cities = City.objects.all()
    city_data = [model_to_dict[city] for city in cities] """
    #fetch_time_results = [fetch_time_task.delay(city['id']) for city in city_data]    
    #fetch_weather_results = [fetch_weather_task.delay(city['id']) for city in city_data]
    
    fetch_time_task_result = fetch_time_task.delay()
    fetch_weather_task_result = fetch_weather_task.delay()
    scraped_exchange_rate = daily_exchange_rate_task.delay

    
    
#    weather_data = [fetch_weather(city) for city in cities]
    
#   time_data = [fetch_time(city) for city in cities]
    
#    applicable_date, currency_to_display = daily_exchange_rate()
    

    weather_time_data = zip(weather_data, time_data)
    context = {
        'weather_time_data': weather_time_data,
        #'applicable_date': applicable_date,
        #'currency_to_display': currency_to_display,
        'rooms': rooms,
    }
    print(f"Inside the views {currency_to_display}")

    

    
 
    return render(request, 'index.html', context)
