from connection_to_database import questions_table, games_table
from support import get_question_order, insert_document, get_themes, get_played_themes


def form_correct_question(question_data):
    question_data.setdefault('order', get_question_order(questions_table, question_data))
    question_data['id'] = question_data['theme'] + str(question_data['order'])
    insert_document(questions_table, question_data.copy())
    return question_data


#def start_game(game_data):

def set_theme(group_id, theme):
    if (theme in get_themes(questions_table)) and \
            (theme not in get_played_themes(games_table, group_id)):
        question_id = theme + str(1)
        games_table.find_one_and_update({'$and': [{'group_id': group_id},
                                                  {'game_finished': False}]},
                                        {'current_theme': theme,
                                         'current_question': question_id,
                                         # TODO: check out the timestamps
                                         'time_finish': None})
        return {'id': question_id}
    else:
        return {'error': 'Theme not found'}


def get_question(id):
    question = questions_table.find_one({'id': id})
    return {'data': question}


#def check_answer(answer):



class Question:
    def __init__(self, theme, points, text, answer):
        self.theme = theme
        self.points = points
        self.text = text
        self.answer = answer


class Game:
    def __init__(self, group_id):
        self.group_id = group_id
