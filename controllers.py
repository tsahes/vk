from connection_to_database import questions_table
from json_responses import json_response, error_json_response
from models import quest_verification
from support import insert_document, get_questions, get_question_order


async def questions_list(request):
    params = request.rel_url.query
    limit = int(request.rel_url.query['limit']) if 'limit' in params else 100
    offset = int(request.rel_url.query['offset']) if 'offset' in params else 0
    theme = request.rel_url.query['theme'] if 'theme' in params else None

    data = get_questions(questions_table, limit, offset, theme)

    return json_response(data={'total' : len(data), 'questions' : data})


async def empty(request):
    return json_response()


async def questions_create(request):
    question = await request.json()
#    pprint(question)
    correct_question = quest_verification(question)

    if correct_question['success']:
        correct_question = correct_question['data']
        correct_question.setdefault('order', get_question_order(questions_table, correct_question))
        correct_question['id'] = correct_question['theme']+str(correct_question['order'])

        insert_document(questions_table, correct_question.copy())
        return json_response(data=correct_question)
    else:
        return error_json_response(text_status='not ok', data=correct_question['data'])


async def questions_delete(request):
    question = await request.json()
    questions_table.delete_one({'id' : question['id']})
    return json_response()

