
from aiohttp import web

from connection_to_vk import api, confirmation_token
from controllers import game_start, get_game_results, set_theme, check_answer
from game_functions import latest_game

'''confirmation_token = 'e9d2702e'
token = os.environ.get('vk_api_token')
session = vk.Session(access_token=token)
api = vk.API(session, v='5.130')'''


async def processing(request):
    data = await request.json()

    if 'type' not in data.keys():
        return web.Response(text='not vk')

    if data['type'] == 'confirmation' and data['group_id'] == 202927298:
        return web.Response(text=confirmation_token)

    elif data['type'] == 'message_new':
        #conversations = api.messages.getConversations()
        message = data['object']['message']
        peer_id = message['peer_id']
        text = message['text']
        user_id = message['from_id']

        group_id = data['group_id']
        result = await get_stage(peer_id, user_id, text)
#        api.messages.send(peer_id=str(peer_id), group_id=group_id,
#                          message=text,
#                          random_id=random.getrandbits(64))
        # Сообщение о том, что обработка прошла успешно
        return web.Response(text='ok')


async def get_stage(group_id, user_id, text):
    game = await latest_game(group_id)
    if game[1] == 'finished':
        if text.lower().find('игр') > -1:
            return await game_start(group_id)
        elif text.lower().find('результат') > -1:
            return await get_game_results(group_id)
    elif game[1] == 'current':
        if game['current_theme'] is None:
            return await set_theme(text, group_id)
        else:
            return await check_answer(text, group_id, user_id)
    return -1
