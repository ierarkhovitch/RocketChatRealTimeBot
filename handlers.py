# -*- coding: utf-8 -*-

import json
import random

import read_tsv
import database
import settings
from weather import parsers


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
    elif message in settings.GREETING:
        with open('files/greeting.json', encoding='utf-8') as file:
            return settings.GREETING_ANSWER, json.load(file)
    elif any(help_trigger for help_trigger in settings.HELP_TRIGGER if help_trigger in message):
        return '', need_help(username)
    # elif '|' in message:
    #     return training_bot(username, message), None
    # elif any(weather_trigger for weather_trigger in settings.WEATHER_TRIGGERS if weather_trigger in message):
    #     return f"Сейчас в Питере: {parsers.weather()}", None
    elif 'курс' in message:
        return parsers.exchange_rates(), None
    elif next_scenario(username, message.capitalize()):
        return '', display_next_scenario(username, message.capitalize())
    else:
        return read_tsv.search_reply(message), None

    # else: database.search_for_a_dialogue(msg, 90):
    #     return database.search_for_a_dialogue(msg, 90), None
    # else:
    #     return database.search_for_a_dialogue(msg, 85), None
    #return random.choice(['Я не знаю что ответить...', 'не понимаю', 'что то не совсем понял']), None


def create_user_status(username):
    """
    Заведение пользователя в базу данных
    :param username: имя пользователя
    """
    if not database.search_user_status(username):
        database.insert_base_user_status('user_status', username, 0, 0)


def training_bot(username, message):
    """
    Обучени бота (занесение триггеров и ответов в базу данных)
    :param username: имя пользователя
    :param message: сообщение
    """
    message = message.lower().split('|')
    if not database.search_message_dialog(message[0]):
        database.insert_base_trigger_answer('trigger_answer', message[0], message[1].capitalize())
        database.insert_base_logging_training('logging_training', message[0], message[1], username)
        return "Запись успешно внесена"
    else:
        return "Такая запись уже сушествует"


def need_help(username):
    """
    Вхождение в набор кнопок
    :param username: имя пользователя
    """
    database.update_base_user_status('user_status', username, 0, 0)
    return json.loads(database.read_base_support(0, 0))


def next_scenario(username, msg):
    """
    Проверка перехода в следующий шаг сценария
    :param username: имя пользователя
    :param msg: сообщение
    """
    data = database.search_user_status(username)[0]
    base = json.loads(database.read_base_support(data[0], data[1]))
    for button in (base[0]['actions']):
        if 'msg' not in button:
            continue
        elif msg == button['msg']:
            return True


def display_next_scenario(username, msg):
    """
    Вывод следующего сценария
    :param username: имя пользователя
    :param msg: сообщение
    """
    data = database.search_user_status(username)[0]
    base = json.loads(database.read_base_support(data[0], data[1]))
    for button in (base[0]['actions']):
        if 'msg' not in button:
            continue
        elif msg == button['msg'] and 'next_scenario' in button:
            database.update_base_user_status('user_status', username, button['next_scenario'], button['next_step'])
            return json.loads(database.read_base_support(button['next_scenario'], button['next_step']))



