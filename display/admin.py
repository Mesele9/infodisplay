from django.contrib import admin
from .models import City, Rooms, Currency, CachedTime, CachedWeather, ExchangeRate


# Register your models here.
admin.site.register(City)
admin.site.register(Rooms)
admin.site.register(Currency)
admin.site.register(CachedTime)
admin.site.register(CachedWeather)
admin.site.register(ExchangeRate)