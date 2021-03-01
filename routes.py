from aiohttp import web
from callback_handler import processing
from controllers import (questions_list, questions_create, questions_delete,
                         empty,
                         game_start, set_theme,
                         check_answer, get_current_question)


def setup_routes(app):
    app.add_routes([web.post('/vk', processing),
                    web.get('/', empty),
                    web.get('/api/questions/list', questions_list),
                    web.post('/api/questions/create', questions_create),
                    web.post('/api/questions/delete', questions_delete),
                    web.post('/api/games/start', game_start),
                    web.post('/api/games/set_theme', set_theme),
                    web.post('/api/games/answer', check_answer),
                    web.post('/api/games/get_question', get_current_question),
                    ])