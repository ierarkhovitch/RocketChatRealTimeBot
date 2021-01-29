# -*- coding: utf-8 -*-

import json
from uuid import uuid4


def uuid():
    """
    Создание уникального id
    """
    return uuid4().hex


def connect():
    """
    Подтверждение установки соединения
    """
    msg = {
        "msg": "connect",
        "version": "1",
        "support": ["1"]
    }
    return json.dumps(msg)


def login(token):
    """
    Вход
    :param token: Уникальный токен бота
    """
    uid = uuid()
    msg = {
        "msg": "method",
        "method": "login",
        "id": uid,
        "params": [
            {
                "resume": token
            }
        ]
    }
    return json.dumps(msg)


def send_text_message(room_id, text, attr=None):
    """
    Отправка сообщения
    :param room_id: id комнаты
    :param text: текст сообщения
    :param attr: кнопки
    """
    uid = uuid()
    mid = uuid()
    msg = {
        'msg': 'method',
        'method': 'sendMessage',
        'id': uid,
        'params': [{
            '_id': mid,
            'rid': room_id,
            'msg': text,
            'attachments': attr
        }]
    }
    return json.dumps(msg)


def sub_notify(user_id):
    """
    Подписка на нотификации пользователя
    :param user_id: имя пользователя
    """
    uid = uuid()
    user_notification = user_id + "/notification"
    msg = {
        "msg": "sub",
        "id": uid,
        "name": "stream-notify-user",
        "params": [
            user_notification,
            False
        ]
    }
    return json.dumps(msg)


def sub_otr(user_id):
    uid = uuid()
    user_notification = user_id + "/otr"
    msg = {
        "msg": "sub",
        "id": uid,
        "name": "stream-notify-user",
        "params": [
            user_notification,
            True
        ]
    }
    return json.dumps(msg)


def sub_webrtc(user_id):
    uid = uuid()
    user_notification = user_id + "/webrtc"
    msg = {
        "msg": "sub",
        "id": uid,
        "name": "stream-notify-user",
        "params": [
            user_notification,
            True
        ]
    }
    return json.dumps(msg)


def sub_subscriptions_changed(user_id):
    uid = uuid()
    user_notification = user_id + "/subscriptions-changed"
    msg = {
        "msg": "sub",
        "id": uid,
        "name": "stream-notify-user",
        "params": [
            user_notification,
            True
        ]
    }
    return json.dumps(msg)


def sub_room(room_id):
    msg = {
        "msg": "sub",
        "id": "unique-id",
        "name": "stream-room-messages",
        "params": [
            room_id,
            True
        ]
    }
    return json.dumps(msg)
