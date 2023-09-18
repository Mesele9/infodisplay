import requests
import json
from bs4 import BeautifulSoup

from .models import ExchangeRate, Currency
import time


def daily_exchange_rate():
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
    return rate_applicable_date, currency_to_display