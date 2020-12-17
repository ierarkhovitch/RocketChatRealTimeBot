# -*- coding: utf-8 -*-

import datetime
import json
import random

import database
import settings
from weather import parsers


def filter_text(text):
    text = text.lower()
    text = [c for c in text if c in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя- ']
    text = ''.join(text)
    return text


def message_handler(username, message):
    """
    :param username:
    :param message:
    :return: answer(txt), attachments(json)
    """
    try:
        msg = filter_text(message)
        if not msg or msg == ' '*len(msg):
            return random.choice(['Я не знаю что ответить...', 'не понимаю', 'что то не совсем понял']), None
        elif msg in settings.GREETING:
            with open('files/greeting.json', encoding='utf-8') as file:
                return settings.GREETING_ANSWER, json.load(file)
        elif msg == 'мне нужна помощь':
            return '', need_help(username)
        elif '|' in message:
            return training_bot(username, message), None
        elif any(weather_trigger for weather_trigger in settings.WEATHER_TRIGGERS if weather_trigger in msg):
            return f"Сейчас в Питере: {parsers.weather()}", None
        elif 'курс' in msg:
            return parsers.exchange_rates(), None
        elif send_next_scenario(username, message):
            return '', next_scenario(username, message)
        elif database.search_for_a_dialogue(msg):
            return database.search_for_a_dialogue(msg), None
        return random.choice(['Я не знаю что ответить...', 'не понимаю', 'что то не совсем понял']), None
    except Exception as exc:
        print(datetime.datetime.now(), exc)


def create_user_status(username):
    if not database.search_user_status(username):
        database.insert_base_user_status('user_status', username, 0, 0)


def training_bot(username, message):
    """
    Обучени бота (занесение триггеров и ответов в базу данных)
    :param username: имя пользователя
    :param message: полное сообщение в формате json
    """
    message = message.lower().split('|')
    if not database.search_message_dialog(message[0]):
        database.insert_base_trigger_answer('trigger_answer', message[0], message[1].capitalize())
        database.insert_base_logging_training('logging_training', message[0], message[1], username)
        return "Запись успешно внесена"
    else:
        return "Такая запись уже сушествует"


def need_help(username):
    database.update_base_user_status('user_status', username, 0, 0)
    return json.loads(database.read_base_support(0, 0))


def send_next_scenario(username, msg):
    data = database.search_user_status(username)[0]
    base = json.loads(database.read_base_support(data[0], data[1]))
    for button in (base[0]['actions']):
        if 'msg' not in button:
            continue
        elif msg == button['msg']:
            return True


def next_scenario(username, msg):
    data = database.search_user_status(username)[0]
    base = json.loads(database.read_base_support(data[0], data[1]))
    for button in (base[0]['actions']):
        if 'msg' not in button:
            continue
        elif msg == button['msg'] and 'next_scenario' in button:
            database.update_base_user_status('user_status', username, button['next_scenario'], button['next_step'])
            return json.loads(database.read_base_support(button['next_scenario'], button['next_step']))



