import requests
import unittest
import json


SUCCESS = 200
INCORRECT_HEADER = 400
ADDED = 201


class TestQuestions(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(TestQuestions, self).__init__(*a, **kw)
        self.host = 'qainterview.cogniance.com'
        self.command = 'candidates'
        self.url = 'http://{}/{}'.format(self.host, self.command)

    def test_data_creation_incorrect_header(self):
        kwargs = {'name': '', 'position': '', 'headers': None}
        status_code, text = self._create_account(**kwargs)
        self.assertEqual(status_code, INCORRECT_HEADER)

    def test_data_creation(self):
        random_name = "{} {}".format(choice(FIRST_NAMES), choice(LAST_NAMES))
        position = "{} {}".format(choice(SENIORITY), choice(POSITIONS))
        kwargs = {'name': random_name, 'position': position}
        status_code, text = self._create_account(**kwargs)
        self.assertEqual(status_code, ADDED)
        self.assertIn(random_name, self._get_list_of('name'))

    def test_data_retrieve(self):
        status_code, accounts = self._get_accounts()
        self.assertEqual(status_code, SUCCESS)
        self.assertGreater(len(accounts.get('candidates')), 1)

        status_code, account = self._get_accounts(identificator=1)
        self.assertEqual(status_code, SUCCESS)
        self.assertTrue(isinstance(account.get('candidate'), dict))

    def test_delete(self):
        identificator = choice(self._get_list_of('id'))
        status_code, text = self._delete_account(identificator)
        self.assertEqual(status_code, SUCCESS)
        self.assertNotIn(identificator, self._get_list_of('id'))

    def _get_accounts(self, identificator=None):
        _url = self.url
        if identificator:
            _url = "{}/{}".format(self.url, identificator)
        _response = requests.get(_url)
        return _response.status_code, _response.json()

    def _get_list_of(self, key):
        _, data = self._get_accounts()
        return map(lambda x: x.get(key), data.get('candidates'))

    def _create_account(self, name, position, headers=DEFAULT_HEADER):
        _headers = {'content-type': headers}
        _payload = json.dumps({'name': name, 'position': position})
        _response = requests.post(self.url, data=_payload, headers=_headers)
        return _response.status_code, _response.json()

    def _delete_account(self, identificator):
        _response = requests.delete("{}/{}".format(self.url, identificator))
        return _response.status_code, _response.json()


if __name__ == '__main__':
    unittest.main(verbosity=2)