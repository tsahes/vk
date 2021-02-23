from aiohttp import web
from controllers import questions_list, questions_create, questions_delete, empty

def setup_routes(app):
    app.add_routes([web.get('/', empty),
                    web.get('/api/questions/list', questions_list),
                    web.post('/api/questions/create', questions_create),
                    web.post('/api/questions/delete', questions_delete)])