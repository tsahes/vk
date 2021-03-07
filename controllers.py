import random
import time
from connection_to_database import questions_table, games_table
from json_responses import json_response, error_json_response
from models import data_verification
from support import insert_document, get_questions, get_game_order, get_themes, gen_game_id, get_played_themes, \
    get_games
from game_functions import (form_correct_question, get_question,
                            check_and_set_theme, find_current_question,
                            answer_is_correct, change_player_points,
                            set_next_question, func_get_current_question,
                            latest_game, present_game_results, check_player_already_answered)
from connection_to_vk import api


# ADMIN API FUNCTIONALITY
async def questions_list(request):
    params = request.rel_url.query
    limit = int(request.rel_url.query['limit']) if 'limit' in params else 100
    offset = int(request.rel_url.query['offset']) if 'offset' in params else 0
    theme = request.rel_url.query['theme'] if 'theme' in params else None

    data = await get_questions(questions_table, limit, offset, theme)

    return json_response(data={'total': len(data), 'questions': data})


async def empty(request):
    return json_response()


async def questions_create(request):
    question = await request.json()
#    pprint(question)
    correct_question = data_verification(question, type='question')

    if correct_question['success']:
        correct_question = correct_question['data']
        correct_question = await form_correct_question(correct_question)
        return json_response(data=correct_question)
    else:
        return error_json_response(text_status='not ok', data=correct_question['data'])


async def questions_delete(request):
    question = await request.json()
    await questions_table.delete_one({'id': question['id']})
    return json_response()


async def games_list(request):
    params = request.rel_url.query
    limit = int(request.rel_url.query['limit']) if 'limit' in params else 100
    offset = int(request.rel_url.query['offset']) if 'offset' in params else 0

    data = await get_games(games_table, limit, offset)

    return json_response(data={'total': len(data), 'games': data})


# GAME FUNCTIONALITY
async def game_start(group_id):
    game_id = gen_game_id(group_id, await get_game_order(games_table, group_id))
    new_game = dict(group_id=group_id,
                    game_id=game_id,
                    players={},
                    game_finished=False,
                    current_theme=None,
                    players_answered=[]
                    )
    correct_game = data_verification(new_game, type='game')
    await insert_document(games_table, correct_game['data'].copy())

    themes = await get_themes(questions_table)
    played_themes = await get_played_themes(games_table, group_id)
    themes = [theme for theme in themes if theme not in played_themes]

    message = 'Выберите тему из списка: ' + ', '.join(themes)
    api.messages.send(message=message, peer_id=group_id, random_id=random.getrandbits(64))
    return 1


async def set_theme(theme, group_id):
    try:
        question_id = await check_and_set_theme(group_id, theme)
        question = await get_question(question_id['id'])
        message = question['text']
        api.messages.send(message=message, peer_id=group_id, random_id=random.getrandbits(64))
    except KeyError as err:
        api.messages.send(message='Не удалось найти выбранную тему. Попробуйте ещё раз.',
                          peer_id=group_id, random_id=random.getrandbits(64))
    return 1


async def check_answer(answer, group_id, user_id):
    finish_time, current_question = await find_current_question(group_id)
    player_answered = await check_player_already_answered(group_id, user_id)

    if player_answered:
        api.messages.send(message='Вы уже отвечали на этот вопрос.',
                          peer_id=group_id, random_id=random.getrandbits(64))

    else:
        if finish_time < time.time()*1000:
            await set_next_question(group_id, current_question)
            api.messages.send(message='Ответ пришел слишком поздно, следующий вопрос:',
                              peer_id=group_id, random_id=random.getrandbits(64))
            await send_current_question(group_id)

        else:
            points = current_question['points']
            correct_answer = await answer_is_correct(answer, current_question['id'])

            if correct_answer:
                await change_player_points(group_id, user_id, points)
                await set_next_question(group_id, current_question)
                api.messages.send(message='Верно. Участник '+str(user_id)+' получает '+str(points)+' очков.',
                                  peer_id=group_id, random_id=random.getrandbits(64))
                await send_current_question(group_id)

            else:
                await change_player_points(group_id, user_id, -points)
                api.messages.send(message='Неверно. Участник '+str(user_id)+' теряет '+str(points)+' очков.',
                                  peer_id=group_id, random_id=random.getrandbits(64))
    return 1


async def send_current_question(group_id):
    question = await func_get_current_question(group_id)
    if question is None:
        api.messages.send(message='Игра закончена. Вы можете посомтреть результаты или начать новую игру.',
                          peer_id=str(group_id), random_id=random.getrandbits(64))
    else:
        message = question['text']
        api.messages.send(message=message, peer_id=group_id, random_id=random.getrandbits(64))
    return 1


async def get_game_results(group_id):
    game = await latest_game(group_id)
    message = present_game_results(game)
    api.messages.send(message=message, peer_id=group_id, random_id=random.getrandbits(64))
    return 1


async def stop_game(group_id):
    await games_table.find_one_and_update({'group_id': group_id, 'game_finished': False},
                                          {'$set': {'game_finished': True,
                                                    'current_question': None,
                                                    'time_finish': None,
                                                    'players_answered': []}}
                                          )
    await get_game_results(group_id)
    return 1