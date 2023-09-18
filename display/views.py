from django.shortcuts import render
from django.http import HttpResponse

from .models import City, Rooms, ExchangeRate
#from .timeapi import fetch_time
from .weatherapi import fetch_weather
from .timeapi import fetch_time
from .scrap import daily_exchange_rate


def index(request):
    cities = City.objects.all()
    rooms = Rooms.objects.all()
    
    weather_data = [fetch_weather(city) for city in cities]
    
    time_data = [fetch_time(city) for city in cities]
    
    applicable_date, currency_to_display = daily_exchange_rate()
    

    weather_time_data = zip(weather_data, time_data)
    context = {
        'weather_time_data': weather_time_data,
        'applicable_date': applicable_date,
        'currency_to_display': currency_to_display,
        'rooms': rooms,
    }
    print(f"Inside the views {currency_to_display}")
    
 
    return render(request, 'index.html', context)
