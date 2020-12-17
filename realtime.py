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

try:
    import settings
except ImportError:
    exit("Need copy settings.py.default settings.py and set token, user_id and url")

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('bot')


class WebSocket:
    def __init__(self, url):
        self.url = url

    def log_message(self, message):
        data = json.loads(message)
        if 'result' in data and 'u' in data['result']:
            print(f"{data['result']['u']['username']} send:  {data['result']['msg']}")
        # log.info(message)

    async def consumer_handler(self, ws):
        async for message in ws:
            if json.loads(message)['msg'] == 'ping':
                await ws.send(json.dumps({'msg': 'pong'}))
            elif json.loads(message)['msg'] == 'changed':
                await self.changed_handler(message, ws)
            else:
                self.log_message(message)

    async def changed_handler(self, message, ws):
        payload = json.loads(message)['fields']['args'][0]['payload']
        username, rid, msg = payload['sender']['username'], payload['rid'], payload['message']['msg']
        print(f"{username} send:  {msg}")
        if username != settings.USER_ID:
            data = {}
            handlers.create_user_status(username)
            data['msg'], data['attr'] = handlers.message_handler(username, msg)
            await ws.send(metods.send_text_message(room_id=rid, text=f"{data['msg']}", attr=data['attr']))
            database.insert_base_bot_log('bot_log', username, msg, data['msg'])

    async def consume(self):
        try:
            async with websockets.connect(self.url, ping_interval=0) as websocket:
                await websocket.send(metods.connect())
                await websocket.send(metods.login(settings.TOKEN))
                await websocket.send(metods.sub_notify(settings.USER_ID))
                await websocket.recv()
                await self.consumer_handler(websocket)
        except Exception as exc:
            database.insert_base_bag_log('bag_log', exc)
            print(datetime.datetime.now(), exc)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    websocket = WebSocket(settings.WSS_URL)
    loop.run_until_complete(websocket.consume())
    loop.run_forever()
