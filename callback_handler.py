import vk
import random
import os
from json_responses import json_response, error_json_response
from aiohttp import web



confirmation_token = 'e9d2702e'
token = os.environ.get('vk_api_token')

#def first_confirmation(request):
#    data = request.json()



async def processing(request):
    #Распаковываем json из пришедшего POST-запроса
    data = await request.json()
    print(data['type'])
    print(data)
    #Вконтакте в своих запросах всегда отправляет поле типа
    if 'type' not in data.keys():
        return web.Response(text='not vk')
    if data['type'] == 'confirmation' and data['group_id'] == 202927298:
        return web.Response(text=confirmation_token)
    elif data['type'] == 'message_new':
        session = vk.Session()
        api = vk.API(session, v='5.80')
        conversations = api.messages.getConversations(access_token=token,)
        print(data['object'].keys())
        if 'from_id' in data['object']:
            user_id = data['object']['from_id']
        else:
            user_id = ''
#        message = data['object']['body']
#        print(message)
        group_id = data['group_id']
        peer_id = data['object']['peer_id']
        if 'chat_id' in data['object'].keys():
            chat_id = data['object']['chat_id']
        else:
            chat_id = ''
        api.messages.send(access_token=token, user_id=str(user_id),
                          peer_id=peer_id, group_id=group_id,
                          chat_id=chat_id, message=str(conversations), random_id=random.getrandbits(64))
        # Сообщение о том, что обработка прошла успешно
        return web.Response(text='ok')