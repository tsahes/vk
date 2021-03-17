from aiohttp import web
from callback_handler import processing
from controllers import (questions_list, questions_create, questions_delete,
                         empty, games_list, games_create, games_delete,
                         )


def setup_routes(app):
    app.add_routes([web.get('/', empty),
                    web.get('/api/questions/list', questions_list),
                    web.get('/api/games/list', games_list),
                    web.post('/api/questions/create', questions_create),
                    web.post('/api/questions/delete', questions_delete),
                    web.post('/vk', processing),
                    # routes and handles for filling up the db with test data
                    web.post('/api/games/create', games_create),
                    web.post('/api/games/delete', games_delete)
                    ])
