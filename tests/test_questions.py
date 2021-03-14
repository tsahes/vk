import requests
import unittest
import aiounittest
import json

from connection_to_database import questions_table
from support import get_question_order, gen_question_id

SUCCESS = 200
INCORRECT_HEADER = 400
ADDED = 201


class TestQuestions(aiounittest.AsyncTestCase):

    def __init__(self, *a, **kw):
        super(TestQuestions, self).__init__(*a, **kw)
        self.host = 'tsahes-svoya-igra.herokuapp.com/api/questions'
        self.commands = ['list', 'create', 'delete']
        self.urls = {command: 'http://{}/{}'.format(self.host, command) for command in self.commands}

    async def test_data_creation(self):
        # random_name = "{} {}".format(choice(FIRST_NAMES), choice(LAST_NAMES))
        # position = "{} {}".format(choice(SENIORITY), choice(POSITIONS))
        # kwargs = {'name': random_name, 'position': position}
        test_question = {'points': 0, 'theme': 'test_theme', 'text': 'test_text',
                         'answers': {'text': 'test_answer', 'id': 0, 'is_correct': True, 'order': 0}}
        order = await get_question_order(questions_table, test_question)
        question_id = gen_question_id(test_question['theme'], order)

        status_code, text = self._create_question(test_question)

        test_question['order'] = order
        test_question['id'] = question_id

        self.assertEqual(status_code, ADDED)
        self.assertEqual(text, test_question)

    # def test_data_retrieve(self):
    #     status_code, accounts = self._get_accounts()
    #     self.assertEqual(status_code, SUCCESS)
    #     self.assertGreater(len(accounts.get('candidates')), 1)
    #
    #     status_code, account = self._get_accounts(identificator=1)
    #     self.assertEqual(status_code, SUCCESS)
    #     self.assertTrue(isinstance(account.get('candidate'), dict))
    #
    # def test_delete(self):
    #     identificator = choice(self._get_list_of('id'))
    #     status_code, text = self._delete_account(identificator)
    #     self.assertEqual(status_code, SUCCESS)
    #     self.assertNotIn(identificator, self._get_list_of('id'))
    #
    # def _get_accounts(self, identificator=None):
    #     _url = self.url
    #     if identificator:
    #         _url = "{}/{}".format(self.url, identificator)
    #     _response = requests.get(_url)
    #     return _response.status_code, _response.json()
    #
    # def _get_list_of(self, key):
    #     _, data = self._get_accounts()
    #     return map(lambda x: x.get(key), data.get('candidates'))
    #
    def _create_question(self, data):
        _response = requests.post(self.urls['create'], data=data)
        return _response.status_code, _response.json()

    # def _delete_account(self, identificator):
    #     _response = requests.delete("{}/{}".format(self.url, identificator))
    #     return _response.status_code, _response.json()


if __name__ == '__main__':
    unittest.main(verbosity=2)