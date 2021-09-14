
import json

import metods
import naumen.api_naumen as naumen


async def create(username, ws, rid):
    ticket = {}
    await ws.send(metods.send_text_message(room_id=rid, text=f"Введите тему обращения"))
    async for message in ws:
        if json.loads(message)['msg'] == 'ping':
            await ws.send(json.dumps({'msg': 'pong'}))
        if json.loads(message)['msg'] == 'changed':
            message = json.loads(message)['fields']['args'][0]['payload']['message']['msg']
            ticket['theme'] = message.replace('?', ' ')
            break
    await ws.send(metods.send_text_message(room_id=rid, text=f"Введите текст обращения"))
    async for message in ws:
        if json.loads(message)['msg'] == 'ping':
            await ws.send(json.dumps({'msg': 'pong'}))
        if json.loads(message)['msg'] == 'changed':
            message = json.loads(message)['fields']['args'][0]['payload']['message']['msg']
            ticket['text'] = message.replace('?', ' ')
            break
    await ws.send(metods.send_text_message(room_id=rid, text=naumen.create_order(username, ticket)))
