from django.test import TestCase
from ..models import City, CachedTime, CachedWeather, Currency, ExchangeRate

class ModelsTestCase(TestCase):
    def setUp(self):
        # Create test data
        self.city = City.objects.create(name='Nairobi', city_timezone='Africa')

    def test_city_model(self):
        self.assertEqual(str(self.city), 'Nairobi: Africa')

    def test_cached_time_model(self):
        cached_time = CachedTime.objects.create(city=self.city, current_time='12:00', current_date='2023-09-26')
        expected_str = '{}: {}'.format(cached_time.city, cached_time.timestamp, cached_time.current_time, cached_time.current_date)
        self.assertEqual(str(cached_time), expected_str)
        
    def test_cached_weather_model(self):
        cached_weather = CachedWeather.objects.create(city=self.city, temprature=25, description='Sunny', icon='01d')
        expected_str = '{}: {}'.format(cached_weather.city, cached_weather.timestamp, cached_weather.temprature, cached_weather.description, cached_weather.icon)
        self.assertEqual(str(cached_weather), expected_str)

    def test_currency_model(self):
        currency = Currency.objects.create(code='USD', name='US Dollar', country='United States')
        self.assertEqual(str(currency), 'USD: United States')

    def test_exchange_rate_model(self):
        currency = Currency.objects.create(code='USD', name='US Dollar', country='United States')
        exchange_rate = ExchangeRate.objects.create(currency=currency, rate=1.0, applicable_date='2023-09-26')
        self.assertEqual(str(exchange_rate), 'USD: United States: 1.0')
