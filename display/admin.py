from django.contrib import admin
from .models import City, Rooms, Currency


# Register your models here.
admin.site.register(City)
admin.site.register(Rooms)
admin.site.register(Currency)