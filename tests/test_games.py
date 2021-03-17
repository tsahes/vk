import requests
import aiounittest
import json

from connection_to_database import games_table
from controllers import game_start
from support import gen_game_id

SUCCESS = 200


class TestGames(aiounittest.AsyncTestCase):

    def __init__(self, *a, **kw):
        super(TestGames, self).__init__(*a, **kw)
        self.host = 'tsahes-svoya-igra.herokuapp.com/api/games'
        self.commands = ['create', 'list', 'delete']
        self.urls = {command: 'http://{}/{}'.format(self.host, command) for command in self.commands}
        self.game_counter = 1

    async def test_data_creation(self):
        test_game = {'group_id': 1000,
                     'players': {}, 'game_finished': False,
                     'current_theme': 'test_theme', 'players_answered': []}
                    # {'points': 0, 'theme': 'test_theme', 'text': 'test_text',
                    #      'answers': {'text': 'test_answer', 'id': 0, 'is_correct': True, 'order': 0}}

        order = self.game_counter
        game_id = gen_game_id(test_game['group_id'], order)

        status_code, text = self._create_game(**test_game)
        test_game['game_id'] = game_id
        self.assertEqual(status_code, SUCCESS)
        self.assertEqual(text['data'], test_game)

    async def test_data_retrieve(self):
        status_code, questions = self._get_games()
        self.assertEqual(status_code, SUCCESS)
        self.assertGreaterEqual(questions.get('data').get('total'), 1)

        params = {'limit': 1, 'offset': None}
        status_code, questions = self._get_games(**params)
        self.assertEqual(status_code, SUCCESS)
        self.assertEqual(questions.get('data').get('total'), 1)

        params['limit'] = None
        params['offset'] = 1
        status_code, questions = self._get_games(**params)
        self.assertEqual(status_code, SUCCESS)
        self.assertEqual(questions.get('data').get('total'), 0)

    def test_delete(self):
        identifier = '1000-1'
        status_code, text = self._delete_game(identifier)
        self.assertEqual(status_code, SUCCESS)
        self.assertNotIn(identifier, self._get_list_of('game_id'))

    def _get_games(self, limit=None, offset=None):
        _payload = {'limit': limit, 'offset': offset}
        _response = requests.get(self.urls['list'], params=_payload)
        return _response.status_code, _response.json()

    def _get_list_of(self, key):
        _, total_response = self._get_games()
        data = total_response['data']
        return map(lambda x: x.get(key), data.get('games'))

    def _create_game(self, group_id, players, game_finished, current_theme, players_answered):
        _payload = json.dumps({'group_id': group_id,
                               'players': players, 'game_finished': game_finished,
                               'current_theme': current_theme, 'players_answered': players_answered})
        _response = requests.post(self.urls['create'], data=_payload)
        self.game_counter += 1
        return _response.status_code, _response.json()

    def _delete_game(self, identifier):
        _payload = json.dumps({'game_id': identifier})
        _response = requests.post(self.urls['delete'], data=_payload)
        print(_response)
        return _response.status_code, _response.json()


if __name__ == '__main__':
    aiounittest.main(verbosity=2)
