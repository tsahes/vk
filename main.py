from aiohttp import web

#VIEW
async def handle_list(request):
    params = request.rel_url.query
    limit = int(request.rel_url.query['limit']) if 'limit' in params else 100
    offset = int(request.rel_url.query['offset']) if 'offset' in params else 0

    print('\n'.join([
        'limit = ' + str(limit),
        'offset = ' + str(offset),
    ]))

#    response = Questions.find().limit(limit).offset(offset)

#    return web.Response(text=str(questions))
    return web.Response(text='success : True')

async def handle(request):
    return web.Response(text="success")

async def handle_post(request):
    global questions
    text = request['data']

    return web.Response(text='success : True')

#APP
app = web.Application()
#ROUTES
app.add_routes([web.get('/api/questions/list', handle_list),
                web.get('/', handle),
                web.add_view('/api/questions/create', handle_post)])

#DATA (while there's no db)
questions = {
  "data": {
    "total": 0,
    "questions": [
      {
        "order": 0,
        "id": "string",
        "points": 0,
        "text": "string",
        "answers": [{
          "order": 0,
          "id": 0,
          "text": "string",
          "is_correct": True
        }]
      }
    ]
  },
  "status": "ok"
}

if __name__ == '__main__':
    web.run_app(app)
