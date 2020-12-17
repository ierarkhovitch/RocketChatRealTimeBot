# -*- coding: utf-8 -*-

import json
from uuid import uuid4


def uuid() -> str:
    return uuid4().hex


def login(token) -> dict:
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


def connect() -> dict:
    msg = {
        "msg": "connect",
        "version": "1",
        "support": ["1"]
    }
    return json.dumps(msg)


def send_text_message(room_id, text, attr=None) -> dict:
    uid = uuid()
    mid = uuid()
    msg = {
        'msg': 'method',
        'method': 'sendMessage',
        'id': uid,
        'params': [{
            'id': mid,
            'rid': room_id,
            'msg': text,
            'attachments': attr
        }]
    }
    return json.dumps(msg)


def sub_notify(user_id) -> dict:
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


def sub_otr(user_id) -> dict:
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


def sub_webrtc(user_id) -> dict:
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


def sub_subscriptions_changed(user_id) -> dict:
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


def sub_room(room_id) -> dict:
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
