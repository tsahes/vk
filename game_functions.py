from connection_to_database import questions_table, games_table
from support import get_question_order, insert_document, get_themes, get_played_themes, gen_question_id, get_game_order, \
    gen_game_id
import time


seconds_to_answer_question = 1 * 60


async def form_correct_question(question_data):
    question_data.setdefault('order', await get_question_order(questions_table, question_data))
    question_data['id'] = gen_question_id(question_data['theme'], question_data['order'])
    await insert_document(questions_table, question_data.copy())
    return question_data


async def check_and_set_theme(group_id, theme):
    all_themes = await get_themes(questions_table)
    played_themes = await get_played_themes(games_table, group_id)

    if (theme in all_themes) and (theme not in played_themes):
        question_id = gen_question_id(theme)
        await games_table.find_one_and_update({'group_id': group_id, 'game_finished': False},
                                              {'$set': {'current_theme': theme,
                                                        'current_question': question_id,
                                                        'time_finish': time.time() * 1000 + seconds_to_answer_question * 1000}})
        return {'id': question_id}
    else:
        raise KeyError('Theme not found')


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


async def check_player_already_answered(group_id, player):
    game = await games_table.find_one({'group_id': group_id, 'game_finished': False})
    if player in game['players_answered']:
        return True
    else:
        game['players_answered'].append(player)
        await games_table.find_one_and_update({'group_id': group_id, 'game_finished': False},
                                              {'$set': {'players_answered': game['players_answered']}})
        return False


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
                                                        'time_finish': None,
                                                        'players_answered': []}})
    else:
        await games_table.find_one_and_update({'group_id': group_id, 'game_finished': False},
                                              {'$set': {'game_finished': True,
                                                        'current_question': None,
                                                        'time_finish': None,
                                                        'players_answered': []}})


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
    player_ids = list(sorted(players.keys(), key=lambda item: item[1], reverse=True))
    if len(player_ids) > 0:
        players_str = f'победитель — {player_ids[0]} — {players[player_ids[0]]} очков\n'
        players_str += '\n'.join([f'{id} — {players[id]}' for id in player_ids[1:]])
    else:
        players_str = 'никто ещё не заработал очков.'
#    players_str = pformat(players)
    if game[1] == 'current':
        message = 'Промежуточные итоги текущей игры: \n' + players_str
    elif game[1] == 'finished':
        message = 'Результаты последней завершённой игры: \n' + players_str
    return message
