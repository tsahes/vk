from controllers import *
from game_functions import latest_game
command_list = []


class Command:
    def __init__(self):
        self.__keys = []
        self.description = ''
        command_list.append(self)

    @property
    def keys(self):
        return self.__keys

    @keys.setter
    def keys(self, mas):
        for k in mas:
            self.__keys.append(k.lower())

    def process(self):
        pass


start_command = Command()

start_command.keys = ['начать игру', 'запустить игру', 'новая игра', 'новая тема']
start_command.description = 'Запустить игру'
start_command.process = game_start


async def get_stage(group_id, user_id, text):
    game = await latest_game(group_id)
    if game[1] == 'finished':
        if text.lower().find('игр') > -1:
            await game_start(group_id)
        elif text.lower().find('результат') > -1:
            await get_game_results(group_id)
    elif game[1] == 'current':
        if game['current_theme'] is None:
            await set_theme(text, group_id)
        else:
            await check_answer(text, group_id, user_id)


def get_answer(body):
    message = "Прости, не понимаю тебя. Напиши 'помощь', чтобы узнать мои команды"
    for command in command_list:
        for k in command.keys:
            if body == k:
                message = command.process()
                return message
    return message
