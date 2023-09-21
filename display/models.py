from django.db import models


class City(models.Model):
    name = models.CharField(max_length=50)
    city_timezone = models.CharField(max_length=50, null=True)

    def __str__(self):
        return "{}: {}".format(self.name, self.city_timezone)


class CachedTime(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    current_time = models.TimeField(null=True, blank=True)
    current_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return "{}: {}".format(self.city, self.timestamp)


class CachedWeather(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    temprature = models.IntegerField(null=True, blank=True)
    descritpion = models.CharField(max_length=100)
    icon = models.CharField(max_length=20)

    def __str__(self):
        return "{}: {}".format(self.city, self.timestamp)


# Room models
class Rooms(models.Model):
    roomType = models.CharField(max_length=50)
    price = models.IntegerField()

    def __str__(self):
        return "{}: {}".format(self.roomType, self.price)
    

# Exchange rate models
class Currency(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    def __str__(self):
        return "{}: {}".format(self.code, self.country)


class ExchangeRate(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=10, decimal_places=4)
    applicable_date = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return "{}: {}".format(self.currency, self.rate)