from pprint import pformat
from aiohttp import web
import random
from connection_to_vk import api, confirmation_token
from controllers import game_start, get_game_results, set_theme, check_answer, stop_game
from game_functions import latest_game


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

        result = await get_stage(int(peer_id), int(user_id), text)
        # Сообщение о том, что обработка прошла успешно
        return web.Response(text='ok')


async def get_stage(group_id, user_id, text):
    game = await latest_game(group_id)
    if text[0] == '/':
        if text == '/старт':
            return await game_start(group_id)
        elif text == '/статистика':
            return await get_game_results(group_id)
        elif text == '/стоп':
            return await stop_game(group_id)
    elif game[1] == 'current':
        if game[0]['current_theme'] is None:
            return await set_theme(text, group_id)
        else:
            return await check_answer(text, group_id, user_id)
    return -1
