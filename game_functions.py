from pprint import pformat
from connection_to_database import questions_table, games_table
from support import get_question_order, insert_document, get_themes, get_played_themes, gen_question_id, get_game_order, \
    gen_game_id
import time

#for debugging purposes
from connection_to_vk import api
import random

seconds_to_answer_question = 30 * 60


async def form_correct_question(question_data):
    question_data.setdefault('order', await get_question_order(questions_table, question_data))
    question_data['id'] = gen_question_id(question_data['theme'], question_data['order'])
    await insert_document(questions_table, question_data.copy())
    return question_data


async def check_and_set_theme(group_id, theme):
    all_themes = await get_themes(questions_table)
    played_themes = await get_played_themes(games_table, group_id)
    little_message = str(all_themes) + ', ' + str(played_themes)
    api.messages.send(peer_id=group_id, random_id=random.getrandbits(64),
                      message=little_message)
    if (theme in all_themes) and (theme not in played_themes):
        question_id = gen_question_id(theme)
        await games_table.find_one_and_update({'group_id': group_id, 'game_finished': False},
                                              {'$set': {'current_theme': theme,
                                                        'current_question': question_id,
                                                        'time_finish': time.time() * 1000 + seconds_to_answer_question * 1000}})
        return {'id': question_id}
    else:
        raise KeyError('Theme not found')
#        return {'error': 'Theme not found'}


async def get_question(question_id):
    question = await questions_table.find_one({'id': question_id}, {'_id': False})
    return question


async def find_current_question(group_id):
    question_id = await games_table.find_one({'group_id': group_id, 'game_finished': False},
                                             {'current_question': True,
                                              'time_finish': True})
    if question_id:

        finish_time = question_id['time_finish']
        question = await get_question(question_id['current_question'])
        return [finish_time, question]
    else:
        return [None, None]


async def answer_is_correct(answer: str, question_id):
    question = await questions_table.find_one({'id': question_id})
    return answer.upper() == question['answers']['text'].upper()


async def change_player_points(group_id, player, points):
    game = await games_table.find_one({'group_id': group_id, 'game_finished': False})
    player = str(player)
    players = game['players']
    if player in players:
        players[player] += points
    else:
        players[player] = points

    await games_table.find_one_and_update({'group_id': group_id, 'game_finished': False},
                                          {'$set': {'players': game['players']}})


async def set_next_question(group_id, current_question,):
    if current_question['order'] < 5:
        question_id = gen_question_id(current_question['theme'], current_question['order']+1)
        await games_table.find_one_and_update({'group_id': group_id, 'game_finished': False},
                                              {'$set': {'current_question': question_id,
                                                        'time_finish': None}})
    else:
        await games_table.find_one_and_update({'group_id': group_id, 'game_finished': False},
                                              {'$set': {'game_finished': True,
                                                        'current_question': None,
                                                        'time_finish': None}})


async def func_get_current_question(group_id):
    finish_time, current_question = await find_current_question(group_id)
    if current_question is not None:
        if finish_time is None or finish_time < time.time()*1000:
            if finish_time is not None:
                await set_next_question(group_id, current_question)
                current_question = await func_get_current_question(group_id)
            await games_table.find_one_and_update({'group_id': group_id, 'game_finished': False},
                                                  {'$set': {'time_finish': time.time() * 1000 + seconds_to_answer_question * 1000}})
        return current_question
    else:
        return None


async def latest_game(group_id):
    game = await games_table.find_one({'group_id': group_id, 'game_finished': False})
    if game is not None:
        return [game, 'current']
    else:
        number_of_games = await get_game_order(games_table, group_id)
        game_id = gen_game_id(group_id, number_of_games-1)
        game = await games_table.find_one({'game_id': game_id})
        return [game, 'finished']


def present_game_results(game):
    players = game[0]['players']
    players = {user: points for user, points in sorted(players.items(), key=lambda item: item[1], reverse=True)}
    players_str = pformat(players)
    if game[1] == 'current':
        message = 'Промежуточные итоги текущей игры: \n' + players_str
    elif game[1] == 'finished':
        message = 'Результаты последней завершённой игры: \n' + players_str
    return message
