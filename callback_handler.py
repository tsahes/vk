import vk
import random
import os
from json_responses import json_response, error_json_response
from aiohttp import web



confirmation_token = '416094e2'
token = os.environ.get('vk_api_token')

#def first_confirmation(request):
#    data = request.json()



async def processing(request):
    #Распаковываем json из пришедшего POST-запроса
    data = await request.json()
    #Вконтакте в своих запросах всегда отправляет поле типа
    if 'type' not in data.keys():
        return web.Response(text='not vk')
    if data['type'] == 'confirmation' and data['group_id'] == 202927298:
        return web.Response(text=confirmation_token)
    elif data['type'] == 'message_new':
        session = vk.Session()
        api = vk.API(session, v='5.50')
        user_id = data['object']['from_id']
        message = data['object']['body']
        api.messages.send(access_token=token, user_id=str(user_id), message=message, random_id=random.getrandbits(64))
        # Сообщение о том, что обработка прошла успешно
        return web.Response(text='ok')