from aiohttp import web
from pymongo import MongoClient, ASCENDING
# pprint library is used to make the output look more pretty
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
    text = await request.json()
    print(text['offset'])

    return web.Response(text='success : True')

#APP
app = web.Application()

#ROUTES
app.add_routes([web.get('/api/questions/list', handle_list),
                web.get('/', handle),
                web.post('/api/questions/create', handle_post)])

# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client = MongoClient(MONGODB_URL)
db=client.vk_game
# Issue the serverStatus command and print the results
serverStatusResult=db.command("serverStatus")
#pprint(serverStatusResult)

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


#print(find_document(db.questions))
#insert_document(db.questions, {'status' : 'not_ok'})

empty_question = {
  "order": 0,
  "text": "string",
  "points": 0,
  "answers": {
    "order": 0,
    "id": 0,
    "text": "string",
    "is_correct": True
  }
}
#insert_document(db.questions, empty_question)
#db.questions.delete_many({'status' : 'not_ok'})

#ADDING A PACKAGE OF QUESTIONS
rel_question_1 = {
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

rel_question_2 = {
    "order": 2,
  "text": 'Именно ТАК звучат по-японски слова "путь богов".',
  "points": 20,
  "answers": {
    "order": 0,
    "id": 0,
    "text":  "СИНТО",
    "is_correct": True
  }
}

rel_question_3 = {
    "order": 3,
  "text": 'Вождь Терииероо, живший на ЭТОМ острове, чрезвычайно обрадовался, когда узнал от Тура Хейердала, что в Скандинавии почти все исповедуют протестантскую веру.',
  "points": 30,
  "answers": {
    "order": 0,
    "id": 0,
    "text":  "ТАИТИ",
    "is_correct": True
  }
}

rel_question_4 = {
    "order": 4,
  "text": 'Три религии: иудаизм, христианство и ислам — нередко объединяют ЭТИМ прилагательным.',
  "points": 40,
  "answers": {
    "order": 0,
    "id": 0,
    "text":  "АВРААМИЧЕСКИЕ",
    "is_correct": True
  }
}

rel_question_5 = {
    "order": 5,
  "text": 'В России исповедующие ЭТУ религию традиционно называют ее "благоверие".',
  "points": 50,
  "answers": {
    "order": 0,
    "id": 0,
    "text":  "ЗОРОАСТРИЗМ",
    "is_correct": True
  }
}

rel_package = [rel_question_1, rel_question_2,
               rel_question_3, rel_question_4,
               rel_question_5]

#for quest in rel_package:
#    insert_document(db.questions, quest)

#pprint(find_document(db.questions, multiple=True))

def getQuestions(collection, limit=100, offset=0):
    results = collection.find({"text": {'$exists': True}}).sort('order', ASCENDING)
    res_list = [r for r in results]
    return res_list[offset:(offset+limit if offset+limit<len(res_list) else len(res_list))]

pprint(getQuestions(db.questions))

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
