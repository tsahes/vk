import requests
import unittest
import aiounittest
import json

from support import gen_question_id

SUCCESS = 200


class TestQuestions(aiounittest.AsyncTestCase):

    def __init__(self, *a, **kw):
        super(TestQuestions, self).__init__(*a, **kw)
        self.host = 'tsahes-svoya-igra.herokuapp.com/api/questions'
        self.commands = ['create', 'list', 'delete']
        self.urls = {command: 'http://{}/{}'.format(self.host, command) for command in self.commands}
        self.question_counter = 1

    async def test_data_creation(self):
        test_question = {'points': 0, 'theme': 'test_theme', 'text': 'test_text',
                         'answers': {'text': 'test_answer', 'id': 0, 'is_correct': True, 'order': 0}}

        # order = await get_question_order(questions_table, test_question)
        order = self.question_counter
        question_id = gen_question_id(test_question['theme'], order)

        status_code, text = self._create_question(**test_question)

        test_question['order'] = order
        test_question['id'] = question_id

        self.assertEqual(status_code, SUCCESS)
        self.assertEqual(text['data'], test_question)

    def test_data_retrieve(self):
        status_code, questions = self._get_questions()
        self.assertEqual(status_code, SUCCESS)
        self.assertGreaterEqual(questions.get('data').get('total'), 1)

        params = {'limit': 1, 'offset': None, 'theme': None}
        status_code, questions = self._get_questions(**params)
        self.assertEqual(status_code, SUCCESS)
        self.assertEqual(questions.get('data').get('total'), 1)

        params['limit'] = None
        params['offset'] = 1
        status_code, questions = self._get_questions(**params)
        self.assertEqual(status_code, SUCCESS)
        self.assertEqual(questions.get('data').get('total'), self.question_counter - 1)

        params['offset'] = None
        params['theme'] = 'test_theme'
        status_code, questions = self._get_questions(**params)
        self.assertEqual(status_code, SUCCESS)
        self.assertIsInstance(questions.get('data').get('questions'), list)

    def test_delete(self):
        identifier = 'test_theme1'
        status_code, text = self._delete_question(identifier)
        self.assertEqual(status_code, SUCCESS)
        self.assertNotIn(identifier, self._get_list_of('id'))

    def _get_questions(self, limit=None, offset=None, theme=None):
        _payload = {'limit': limit, 'offset': offset, 'theme': theme}
        _response = requests.get(self.urls['list'], params=_payload)
        return _response.status_code, _response.json()

    def _get_list_of(self, key):
        _, total_response = self._get_questions()
        data = total_response['data']
        return map(lambda x: x.get(key), data.get('questions'))

    def _create_question(self, points, theme, text, answers):
        _payload = json.dumps({'points': points, 'theme': theme, 'text': text, 'answers': answers})
        _response = requests.post(self.urls['create'], data=_payload)
        self.question_counter += 1
        return _response.status_code, _response.json()

    def _delete_question(self, identifier):
        _payload = json.dumps({'id': identifier})
        _response = requests.post(self.urls['delete'], data=_payload)
        print(_response)
        return _response.status_code, _response.json()


if __name__ == '__main__':
    aiounittest.main(verbosity=2)