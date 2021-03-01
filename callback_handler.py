import vk
import random
import os


confirmation_token = '416094e2'
token = os.environ.get('vk_api_token')

def processing(request):
    #Распаковываем json из пришедшего POST-запроса
    data = request.json()
    #Вконтакте в своих запросах всегда отправляет поле типа
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation' and data['group_id'] == 202927298:
        return confirmation_token
    elif data['type'] == 'message_new':
        session = vk.Session()
        api = vk.API(session, v='5.50')
        user_id = data['object']['from_id']
        message = data['object']['body']
        api.messages.send(access_token=token, user_id=str(user_id), message=message, random_id=random.getrandbits(64))
        # Сообщение о том, что обработка прошла успешно
        return 'ok'