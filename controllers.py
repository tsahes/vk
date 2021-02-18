from connection_to_database import questions_table, games_table
from json_responses import json_response, error_json_response
from models import quest_verification, gameSchema
from support import insert_document, get_questions, get_question_order, get_game_order, get_themes


async def questions_list(request):
    params = request.rel_url.query
    limit = int(request.rel_url.query['limit']) if 'limit' in params else 100
    offset = int(request.rel_url.query['offset']) if 'offset' in params else 0
    theme = request.rel_url.query['theme'] if 'theme' in params else None

    data = get_questions(questions_table, limit, offset, theme)

    return json_response(data={'total' : len(data), 'questions' : data})


async def empty(request):
    return json_response()


async def questions_create(request):
    question = await request.json()
#    pprint(question)
    correct_question = quest_verification(question)

    if correct_question['success']:
        correct_question = correct_question['data']
        correct_question.setdefault('order', get_question_order(questions_table, correct_question))
        correct_question['id'] = correct_question['theme']+str(correct_question['order'])

        insert_document(questions_table, correct_question.copy())
        return json_response(data=correct_question)
    else:
        return error_json_response(text_status='not ok', data=correct_question['data'])


async def questions_delete(request):
    question = await request.json()
    questions_table.delete_one({'id' : question['id']})
    return json_response()


async def game_start(request):
    game_data = await request.json()
    new_game = dict(group_id=game_data['group_id'],
                    game_finished=False,
                    game_id=str(game_data['group_id'])+str(get_game_order(games_table, game_data)))
    schema = gameSchema()
    game = schema.load(new_game)
    insert_document(games_table, game.copy())
    themes = get_themes(questions_table)
    return json_response(data=themes)


async def themes_list(request):
    params = request.rel_url.query
    limit = int(request.rel_url.query['limit']) if 'limit' in params else 100
    offset = int(request.rel_url.query['offset']) if 'offset' in params else 0

    data = get_themes(questions_table, limit, offset)

    return json_response(data={'total': len(data), 'themes': data})


async def game_with_theme(request):
    message = await request.json()
    theme = message['object']['body']
    # TODO: add already played themes somewhere?
    if theme in get_themes(questions_table):
        question_id = theme + str(1)
        games_table.find_one_and_update({'$and': [{'group_id': message['group_id']},
                                                  {'game_finished': False}]},
                                        {'current_theme': theme,
                                         'current_question': question_id,
                                         # TODO: check out the timestamps
                                         'time_finish': None})
        return json_response(data=questions_table.find_one({'id': question_id}))
    else:
        return error_json_response(data={'error': 'Theme not found'})