import json
from datetime import date
from pprint import pprint

import requests

import xmltodict

import metods


async def rates_exchange(date_now, ws, rid):
    await ws.send(metods.send_text_message(room_id=rid, text=f"Выберете валюту\n{rates(date_now)[1]}"))
    async for message in ws:
        if json.loads(message)['msg'] == 'ping':
            await ws.send(json.dumps({'msg': 'pong'}))
        if json.loads(message)['msg'] == 'changed':
            message = json.loads(message)['fields']['args'][0]['payload']['message']['msg'].upper()
            rate = rates(date_now)
            await ws.send(metods.send_text_message(room_id=rid, text=f"Курс валюты на {rate[0]}{rate[2][message][0]} "
                                                                     f"- {rate[2][message][1]}"))
            break


def rates(date_now):
    rates_name = str()
    rates_value = dict()
    url = f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={date_now}"
    response = requests.get(url).text
    xml = xmltodict.parse(response)
    date_rates = f"{xml['ValCurs']['@Date']}\n"
    for i in xml['ValCurs']['Valute']:
        rates_name += f"{i['CharCode']} - {i['Name']}\n"
        rates_value[i['CharCode']] = [i['Name'], i['Value']]
    return date_rates, rates_name, rates_value
