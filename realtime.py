# -*- coding: utf-8 -*-
from pprint import pprint

import websockets
import datetime
import asyncio
import logging
import json

import database
import handlers
import metods
import naumen.api_naumen as naumen
from create_tiket.ticket import create

try:
    import settings
except ImportError:
    exit("Need copy settings.py.default settings.py and set token, user_id and url")

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('bot')


def filter_text(text):
    """
    Фильтрация сообщения
    :param text: сообщение
    """
    text = text.lower()
    text = [c for c in text if c in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя- ']
    text = ''.join(text)
    return text


class WebSocket:
    def __init__(self, url):
        self.url = url

    def log_message(self, message):
        data = json.loads(message)
        if 'result' in data and 'u' in data['result']:
            print(f"{data['result']['u']['username']} send:  {data['result']['msg']}")
        # log.info(message)

    async def ping_pong(self, ws):
        async for message in ws:
            if json.loads(message)['msg'] == 'ping':
                await ws.send(json.dumps({'msg': 'pong'}))
            elif json.loads(message)['msg'] == 'changed':
                message = json.loads(message)['fields']['args'][0]['payload']
                username, rid, = message['sender']['username'], message['rid'],
                # msg = filter_text(message['message']['msg'])
                msg = message['message']['msg']
                if msg.lower() == 'создать заявку':
                #if any(create_ticket for create_ticket in settings.CREATE_TICKET if create_ticket in msg.lower()):
                    await create(username, ws, rid)
                else:
                    await self.changed_handler(username, rid, msg, ws)
            else:
                self.log_message(message)

    # async def create_ticket(self, username, ws, rid):
    #     ticket = {}
    #     await ws.send(metods.send_text_message(room_id=rid, text=f"Ведите тему обращения"))
    #     async for message in ws:
    #         if json.loads(message)['msg'] == 'changed':
    #             message = json.loads(message)['fields']['args'][0]['payload']['message']['msg']
    #             ticket['theme'] = message
    #             break
    #     await ws.send(metods.send_text_message(room_id=rid, text=f"Ведите текст обращения"))
    #     async for message in ws:
    #         if json.loads(message)['msg'] == 'changed':
    #             message = json.loads(message)['fields']['args'][0]['payload']['message']['msg']
    #             ticket['text'] = message
    #             break
    #     await ws.send(metods.send_text_message(room_id=rid, text=naumen.create_order(username, ticket)))

    async def changed_handler(self, username, rid, msg, ws):
        print(f"{username} send:  {msg}")
        if username != settings.USER_ID:
            data = {}
            # handlers.create_user_status(username)
            data['msg'], data['attr'] = handlers.message_handler(username, msg)
            await ws.send(metods.send_text_message(room_id=rid, text=f"{data['msg']}", attr=data['attr']))
            database.insert_base_bot_log('bot_log', username, msg, data['msg'])

    async def consume(self):
        async with websockets.connect(self.url) as websocket:
            await websocket.send(metods.connect())
            await websocket.send(metods.login(settings.TOKEN))
            await websocket.send(metods.sub_notify(settings.USER_ID))
            await websocket.recv()
            await self.ping_pong(websocket)


if __name__ == '__main__':
    while True:
        try:
            loop = asyncio.get_event_loop()
            websocket = WebSocket(settings.WSS_URL)
            loop.run_until_complete(websocket.consume())
            loop.run_forever()
        except Exception as exc:
            # database.insert_base_bag_log('bag_log', exc)
            print(datetime.datetime.now(), exc)
            print(exc.__str__())
            continue
