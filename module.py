from connection_to_database import questions_table, games_table
from support import get_question_order, insert_document, get_themes, get_played_themes, gen_question_id
import time


async def form_correct_question(question_data):
    question_data.setdefault('order', get_question_order(questions_table, question_data))
    question_data['id'] = gen_question_id(question_data['theme'], question_data['order'])
    await insert_document(questions_table, question_data.copy())
    return question_data


async def check_and_set_theme(group_id, theme):
    if (theme in await get_themes(questions_table)) and \
            (theme not in await get_played_themes(games_table, group_id)):
        question_id = gen_question_id(theme)
        await games_table.find_one_and_update({'$and': [{'group_id': group_id},
                                                        {'game_finished': False}]},
                                              {'current_theme': theme,
                                               'current_question': question_id,
                                               'time_finish': time.time()*1000 + 2*60*1000})
        return {'id': question_id}
    else:
        raise KeyError('Theme not found')
#        return {'error': 'Theme not found'}


async def get_question(question_id):
    question = await questions_table.find_one({'id': question_id})
    return question


async def find_current_question(group_id):
    question = await games_table.find_one({'$and': [{'group_id': group_id},
                                                    {'game_finished': False},
                                                    {'time_finish': {'$gte': time.time()}}]},
                                          {'current_question': {'$exists': True}})
    return question


async def answer_is_correct(answer: str, question_id):
    question = await questions_table.find_one({'id': question_id})
    return answer.upper() == question['answer']['text']


async def change_player_points(group_id, player, points):
    game = await games_table.find_one({'$and': [{'group_id': group_id},
                                                {'game_finished': False}]})
    if player in game['players']:
        game['players'] += points
    else:
        game['players'] = points

    await games_table.find_one_and_update({'$and': [{'group_id': group_id},
                                                    {'game_finished': False}]},
                                          {'players': game['players']})


async def set_next_question(group_id, current_question,):
    if current_question['order'] < 5:
        question_id = gen_question_id(current_question['theme'], current_question['order']+1)
        await games_table.find_one_and_update({'$and': [{'group_id': group_id},
                                                        {'game_finished': False}]},
                                              {'current_question': question_id})
    else:
        await games_table.find_one_and_update({'$and': [{'group_id': group_id},
                                                        {'game_finished': False}]},
                                              {'game_finished': True,
                                               'current_theme': None})
        # TODO: need to send game results to the chat


class Question:
    def __init__(self, theme, points, text, answer):
        self.theme = theme
        self.points = points
        self.text = text
        self.answer = answer


class Game:
    def __init__(self, group_id):
        self.group_id = group_id
