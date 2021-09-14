import json
from datetime import date
from pprint import pprint

from bs4 import BeautifulSoup
import requests


def weather():
    response = requests.get(
        r'https://yandex.ru/pogoda/saint-petersburg?utm_campaign=informer&utm_content=main_informer&utm_medium='
        r'web&utm_source=home&utm_term=main_number')
    html_doc = BeautifulSoup(response.text, features='html.parser')
    text = html_doc.find_all("div", {"class": "fact__temp-wrap"})
    pprint(text)
    for element in text:
        temperature = element.find('span', class_="temp__value")
        weather = element.find('div', class_="link__condition day-anchor i-bem")
        return f'{temperature.text} {weather.text}'

