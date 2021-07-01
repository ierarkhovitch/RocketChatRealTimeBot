# -*- coding: utf-8 -*-

import json
import random
from pprint import pprint

import read_tsv
import settings
from test_scenario_excel import scenario
from weather import parsers
from naumen.api_naumen import find_accidents


def filter_text(text):
    """
    Фильтрация сообщения
    :param text: сообщение
    """
    text = text.lower()
    text = [c for c in text if c in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя- ']
    text = ''.join(text)
    return text


def message_handler(username, message):
    """
    Обработка сообщения
    :param username: имя пользователя
    :param message: сообщение
    :return: answer(txt), attachments(json)
    """
    if not message or message == ' '*len(message):
        return random.choice(['Я не знаю что ответить...', 'не понимаю', 'что то не совсем понял']), None
    elif any(greeting_trigger for greeting_trigger in settings.GREETING if greeting_trigger in message.lower()):
        with open('files/greeting.json', encoding='utf-8') as file:
            return settings.GREETING_ANSWER + \
                   f"\nНа данный момент наблюдается аварий: {len(find_accidents())}", json.load(file)
    elif message.lower() == 'информация по авариям':
        answer = ''
        for ticket in find_accidents():
            answer += f"{ticket}\n"
        return answer, None
    elif any(help_trigger for help_trigger in settings.HELP_TRIGGER if help_trigger in message.lower()):
        return '', return_button('Мне нужна помощь')
    elif message.capitalize() in scenario.init_buttons(path='./test_scenario_excel/scenario.xlsx'):
        return '', return_button(message)
    # elif '|' in message:
    #     return training_bot(username, message), None
    # elif any(weather_trigger for weather_trigger in settings.WEATHER_TRIGGERS if weather_trigger in message):
    #     return f"Сейчас в Питере: {parsers.weather()}", None
    elif 'курс' in message:
        return parsers.exchange_rates(), None
    else:
        return read_tsv.search_reply(message), None


def return_button(msg, path='./test_scenario_excel/scenario.xlsx'):
    button = scenario.init_buttons(path)[msg.capitalize()]
    scn = scenario.init_scene(path)
    return [scn[button['scenario']]]


