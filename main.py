from aiohttp import web
from pymongo import MongoClient, ASCENDING, DESCENDING
from marshmallow import Schema, fields, ValidationError, INCLUDE
from pprint import pprint
from creds import MONGODB_URL

# VIEW
async def handle_list(request):
    params = request.rel_url.query
    limit = int(request.rel_url.query['limit']) if 'limit' in params else 100
    offset = int(request.rel_url.query['offset']) if 'offset' in params else 0
    theme = request.rel_url.query['theme'] if 'theme' in params else None

    print('\n'.join([
        'limit = ' + str(limit),
        'offset = ' + str(offset),
    ]))

    data = getQuestions(questions_table, limit, offset, theme)

    return json_response(data={'total' : len(data), 'questions' : data})


async def handle(request):
    return json_response()


async def handle_post(request):
    question = await request.json()
#    pprint(question)
    correct_question = quest_verification(question)

    if correct_question['success']:
        correct_question = correct_question['data']
        correct_question.setdefault('order', getQuestionOrder(questions_table, correct_question))
        correct_question['_id'] = correct_question['theme']+str(correct_question['order'])

        insert_document(db.questions, correct_question)
        return json_response(data=correct_question)
 #       return web.Response(text=str({'data' : correct_question, 'status' : 'ok'}))
    else:
        return error_json_response(text_status='not ok', data=correct_question['data'])


async def handle_delete(request):
    question = await request.json()
    db.questions.delete_one({'_id' : question['id']})
    return json_response()


#JSON RESPONSES
def json_response(
        status: int = 200, text_status: str = "ok", data: dict = None
) -> web.Response:
    return web.json_response(status=status, data={"data": data, "status": text_status})


def error_json_response(
    status: int = 400,
    text_status: str = "ok",
    message: str = "Bad request",
    data: dict = None,
) -> web.Response:
    return web.json_response(
        status=status, data={"data": data, "status": text_status, "message": message}
    )


#APP
app = web.Application()

#ROUTES
app.add_routes([web.get('/api/questions/list', handle_list),
                web.get('/', handle),
                web.post('/api/questions/create', handle_post),
                web.post('/api/questions/delete', handle_delete)])


#CONNECTION TO A DATABASE
client = MongoClient(MONGODB_URL)
db=client.vk_game
# Issue the serverStatus command and print the results
serverStatusResult=db.command("serverStatus")
#pprint(serverStatusResult)
questions_table = db.questions

def insert_document(collection, data):
    """ Function to insert a document into a collection and
    return the document's id.
    """
    return collection.insert_one(data).inserted_id


def find_document(collection, elements={}, multiple=False):
    """ Function to retrieve single or multiple documents from a provided
    Collection using a dictionary containing a document's elements.
    """
    if multiple:
        results = collection.find(elements)
        return [r for r in results]
    else:
        return collection.find_one(elements)


def getQuestions(collection, limit=100, offset=0, theme=None):
    #limit = limit+offset
    if theme:
        results = collection.find({"$and": [{"text": {'$exists': True}},
                                           {"theme": theme}]}
                                  ).sort('order', DESCENDING
                                         ).limit(limit).skip(offset)
    else:
        results = collection.find({"text": {'$exists': True}}
                                  ).sort([('theme', DESCENDING), ('order', DESCENDING)]
                                         ).limit(limit).skip(offset)
    res_list = [r for r in results]
    return res_list[offset:]


def getQuestionOrder(collection, question):
    last_question = getQuestions(collection, limit=1, theme=question['theme'])
    if len(last_question) > 0:
        return last_question[0]['order'] + 1
    else:
        return 1



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

#DATA VERIFICATION
class answerSchema(Schema):
    class Meta:
        unknown = INCLUDE
    text = fields.Str(required=True, error_messages={'required' : 'Answer to the question is required'})
    id = fields.Integer(default=0)
    is_correct = fields.Boolean(default=True)
    order = fields.Integer(default=0)


class questionSchema(Schema):
    class Meta:
        unknown = INCLUDE
    points = fields.Integer()
    theme = fields.Str(required=True, error_messages={'required' : 'Theme is required'})
    text = fields.Str(required=True, error_messages={'required' : 'Text of the question is required'})
    answers = fields.Nested(answerSchema())
#    order = fields.Integer(default=0)


def quest_verification(question):
    schema = questionSchema()

    try:
        result = schema.load(question)
#        pprint(result)
#        correct_question = schema.dump(result)
        return dict(success=True, data=result)
    except ValidationError as err:
        return dict(success=False, data=err.messages)


#print(quest_verification(rel_question_1))

if __name__ == '__main__':
    web.run_app(app)
