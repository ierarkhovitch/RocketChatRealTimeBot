# -*- coding: utf-8 -*-

import datetime
import random
import sqlite3
from pprint import pprint

from fuzzywuzzy import fuzz
from fuzzywuzzy import process


def create_table(table_name):
    """
    Создание таблицы
    """
    conn = sqlite3.connect("dialog.db")
    cursor = conn.cursor()
    cursor.execute(f"CREATE TABLE {table_name} (datetime text, user text, send text, get text)")
    conn.commit()
    conn.close()


def add_data(table_name, data):
    """
    :data: list_tuples (str(trigger), str(answer)), use "|" between elements
    """
    rows = '?,' * len(data[0])
    conn = sqlite3.connect("../dialog.db")
    cursor = conn.cursor()
    cursor.executemany(f"INSERT INTO {table_name} VALUES ({rows[:-1]})", data)
    conn.commit()
    conn.close()


def read_base_support(scenario, step):
    """
    Чтение данных из базы сценариев техподдержки
    """
    conn = sqlite3.connect("./dialog.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT attachments FROM support WHERE scenario = {scenario} and step = {step};")
    support = cursor.fetchall()[0][0]
    conn.close()
    return support


def read_base_dialog():
    """
    Чтение данных из базы простого диалога
    """
    conn = sqlite3.connect("dialog.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM trigger_answer")
    base = cursor.fetchall()
    conn.close()
    return base


def search_message_dialog(message):
    """
    Чтение данных из базы простого диалога
    """
    conn = sqlite3.connect("dialog.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT answer FROM trigger_answer WHERE trigger like '%{message}%'")
    message = cursor.fetchall()
    conn.close()
    return message


def search_for_a_dialogue(message, percent):
    """
    Расстояние левенштейна
    :param message:
    :return:
    """
    data = dict()
    for _ in read_base_dialog():
        search = process.extractOne(message, list(_)[0].split('|'))
        if search[1] >= percent:
            data[search[1]] = _[1]
    return random.choice(data[max(data)].split('|'))
            # return random.choice(_[1].split('|'))

# print(search_for_a_dialogue('ты его не знаешь', 90))

def search_user_status(user):
    """
    Поиск статуса пользователя
    """
    conn = sqlite3.connect("./dialog.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT scenario, step FROM user_status WHERE name = '{user}';")
    user_status = cursor.fetchall()
    conn.close()
    return user_status


def update_base_user_status(table_name, user_name, scenario, step):
    """
    Обновить статус пользователя
    """
    conn = sqlite3.connect("./dialog.db")
    cursor = conn.cursor()
    cursor.execute(f"UPDATE {table_name} SET scenario = '{scenario}', step = '{step}' WHERE name = '{user_name}'")
    conn.commit()
    conn.close()


def insert_base_user_status(table_name, user_name, scenario, step):
    """
    Добавить пользователя со статусом в базу
    """
    conn = sqlite3.connect("./dialog.db")
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO {table_name} (name, scenario, step) VALUES('{user_name}', '{scenario}', '{step}')")
    conn.commit()
    conn.close()


def insert_base_bot_log(table_name, user, send, get):
    """
    Сохранение логов
    """
    time = str(datetime.datetime.now())[:-7]
    conn = sqlite3.connect("./dialog.db")
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO {table_name} (datetime, user, send, get) "
                   f"VALUES('{time}', '{user}', '{send}', '{get}')")
    conn.commit()
    conn.close()


def insert_base_bag_log(table_name, exception):
    """
    Сохранение логов ошибок
    """
    date = str(datetime.datetime.now())[:-7]
    conn = sqlite3.connect("./dialog.db")
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO {table_name} (datetime, exception) "
                   f"VALUES('{date}', '{exception}')")
    conn.commit()
    conn.close()


def insert_base_trigger_answer(table_name, trigger, answer):
    """
    Запись триггеров и ответов
    """
    conn = sqlite3.connect("./dialog.db")
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO {table_name} (trigger, answer) VALUES('{trigger}', '{answer}')")
    conn.commit()
    conn.close()


def insert_base_logging_training(table_name, trigger, answer, username):
    """
    Запись логов обучения
    """
    conn = sqlite3.connect("./dialog.db")
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO {table_name} (trigger, answer, username) "
                   f"VALUES('{trigger}', '{answer}', '{username}')")
    conn.commit()
    conn.close()
