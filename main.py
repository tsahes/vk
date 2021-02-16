from aiohttp import web
from pymongo import MongoClient, ASCENDING, DESCENDING
from marshmallow import Schema, fields, ValidationError, INCLUDE
from pprint import pprint
from creds import MONGODB_URL

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
    question = await request.json()
    pprint(question)
    correct_question = quest_verification(question)
    if correct_question:
        insert_document(db.questions,correct_question)
        return web.Response(text=str({'data' : correct_question, 'status' : 'ok'}))
    else:
        return web.Response(text='success : False')



#APP
app = web.Application()

#ROUTES
app.add_routes([web.get('/api/questions/list', handle_list),
                web.get('/', handle),
                web.post('/api/questions/create', handle_post)])


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
    limit = limit+offset
    if theme:
        results = collection.find({"$and": [{"text": {'$exists': True}},
                                           {"theme": theme}]}
                                  ).sort('order', DESCENDING
                                         ).limit(limit)
    else:
        results = collection.find({"text": {'$exists': True}}
                                  ).sort([('theme', DESCENDING), ('order', DESCENDING)]
                                         ).limit(limit)
    res_list = [r for r in results]
    return res_list[offset:]

def getOrder(collection, question):
    last_question = getQuestions(collection, limit=1, theme=question['theme'])
    if len(last_question) > 0:
        return last_question[0]['order'] + 1
    else:
        return 1

rel_question_1 = {
    'theme' : 'Религиозная',
    "order": 1,
  "text": 'ЭТО сленговое американское выражение, говорящее о потере терпения, принесло две премии "Грэмми" группе "R.E.M."',
  "points": 10,
  "answers": {
    "order": 0,
    "id": 0,
    "text":  "LOSING MY RELIGION",
    "is_correct": True
  }
}
print(rel_question_1['order'])

#pprint(getQuestions(db.questions))

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


def quest_verification(question):
    schema = questionSchema()
#    question.setdefault('order', getOrder(questions_table, question))

    try:
        result = schema.load(question)
        pprint(result)
        correct_question = schema.dump(result)
        return correct_question
    except ValidationError as err:
        pprint(err.messages)


if __name__ == '__main__':
    web.run_app(app)
