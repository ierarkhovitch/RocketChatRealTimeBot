# -*- coding: utf-8 -*-

import json
import random

import read_tsv
import settings
from test_scenario_excel import scenario
from naumen.api_naumen import find_accidents, find_user_tickets, find_announcement


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
    message = message.lower()
    if not message or message == ' '*len(message):
        return random.choice(['Я не знаю что ответить...', 'не понимаю', 'что то не совсем понял']), None
    elif any(greeting_trigger for greeting_trigger in settings.GREETING if greeting_trigger in message):
        with open('files/greeting.json', encoding='utf-8') as file:
            return settings.GREETING_ANSWER + \
                   f"\nНа данный момент наблюдается аварий: {len(find_accidents(username))}", json.load(file)
    elif message == 'об авариях':
        return return_ticket_info(find_accidents, username)
    elif message == "мои заявки":
        return return_ticket_info(find_user_tickets, username)
    elif message == "что умеет робби?":
        return settings.SKILLS, None
    elif message.capitalize() in scenario.init_buttons(path='./test_scenario_excel/scenario.xlsx'):
        return '', return_button(message)
    # elif message == 'анонсы':
    #     return find_announcement(username), None
    else:
        return read_tsv.search_reply(message), None


def return_ticket_info(search, username):
    answer = ''
    tickets = search(username)
    if len(tickets) == 0:
        return "Действующих заявок не найдено", None
    # elif search == find_accidents:
    #     answer += find_announcement(username)
    for ticket in tickets:
        answer += f"{ticket}"
    return answer, None


def return_button(msg, path='./test_scenario_excel/scenario.xlsx'):
    button = scenario.init_buttons(path)[msg.capitalize()]
    scn = scenario.init_scene(path)
    return [scn[button['scenario']]]


