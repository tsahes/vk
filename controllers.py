import time
from connection_to_database import questions_table, games_table
from json_responses import json_response, error_json_response
from models import data_verification
from support import insert_document, get_questions, get_game_order, get_themes, gen_game_id
from module import (form_correct_question, get_question,
                    check_and_set_theme, find_current_question,
                    answer_is_correct, change_player_points,
                    set_next_question, func_get_current_question)


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
    await questions_table.delete_one({'id' : question['id']})
    return json_response()


async def game_start(request):
    game_data = await request.json()
    group_id = game_data['group_id']
    game_id = gen_game_id(group_id, await get_game_order(games_table, group_id))
    new_game = dict(group_id=game_data['group_id'],
                    game_id=game_id,
                    players={},
                    game_finished=False,
                    )
    correct_game = data_verification(new_game, type='game')
    await insert_document(games_table, correct_game['data'].copy())
    themes = await get_themes(questions_table)
    return json_response(data=themes)


async def themes_list(request):
    params = request.rel_url.query
    limit = int(request.rel_url.query['limit']) if 'limit' in params else 100
    offset = int(request.rel_url.query['offset']) if 'offset' in params else 0

    data = await get_themes(questions_table, limit, offset)

    return json_response(data={'total': len(data), 'themes': data})


async def set_theme(request):
    message = await request.json()
    theme = message['object']['body']
    group_id = message['group_id']
    try:
        question_id = await check_and_set_theme(group_id, theme)
        question = await get_question(question_id['id'])
        return json_response(data=question)
    except KeyError as err:
        return error_json_response(data={'error': err.args})


async def check_answer(request):
    message = await request.json()
    answer = message['object']['body']
    group_id = message['group_id']
    user_id = message['object']['user_id']
    finish_time, current_question = await find_current_question(group_id)

    if finish_time < time.time()*1000:
        await set_next_question(group_id, current_question)
        return json_response(data={'error': 'The answer is too late'})
    else:
        points = current_question['points']
        correct_answer = await answer_is_correct(answer, current_question['id'])
        if correct_answer:
            await change_player_points(group_id, user_id, points)
            await set_next_question(group_id, current_question)
            return json_response(data={'message': 'Верно. Участник '+str(user_id)+' получает '+str(points)+' очков.'})
        else:
            await change_player_points(group_id, user_id, -points)
            return json_response(data={'message': 'Неверно. Участник '+str(user_id)+' теряет '+str(points)+' очков.'})


async def get_current_question(request):
    message = await request.json()
    group_id = message['group_id']
    question = await func_get_current_question(group_id)
    if question is None:

        return json_response(data={'error': 'Please start new game'})
    else:
        return json_response(data=question)


async def get_game_results(request):
    message = await request.json()
    group_id = message['group_id']

