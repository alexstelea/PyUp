__author__ = 'alexstelea'

import unittest
from PyUp import UpAPI
import webbrowser


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.j = UpAPI()
        self.access_token = ''
        self.maxDiff = None

    def test_get_band_events(self):
        band_events = self.j.get_band_events(self.access_token)
        band_events_generic = self.j.get_generic_api_call(self.access_token, endpoint='/users/@me/bandevents')
        self.assertIs(band_events['meta']['code'], 200)
        self.assertIs(band_events_generic['meta']['code'], 200)

    def test_get_user_goals(self):
        goals = self.j.get_user_goals(self.access_token)
        goals_generic = self.j.get_generic_api_call(self.access_token, endpoint='/users/@me/goals')
        self.assertIs(goals['meta']['code'], 200)
        self.assertIs(goals_generic['meta']['code'], 200)

    def test_get_resting_heartrate(self):
        data = self.j.get_resting_heartrate(self.access_token)
        data_generic = self.j.get_generic_api_call(self.access_token, endpoint='/users/@me')
        self.assertIs(data['meta']['code'], 200)
        self.assertIs(data_generic['meta']['code'], 200)
        self.assertIsNotNone(data['data'])
        self.assertIsNotNone(data_generic['data'])

    def test_get_user_details(self):
        data = self.j.get_user_details(self.access_token)
        data_generic = self.j.get_generic_api_call(self.access_token, endpoint='/users/@me')
        self.assertIs(data['meta']['code'], 200)
        self.assertIs(data_generic['meta']['code'], 200)
        self.assertIsNotNone(data['data'])
        self.assertIsNotNone(data_generic['data'])

    def test_get_workouts_list(self):
        data = self.j.get_workouts_list(self.access_token)
        data_generic = self.j.get_generic_api_call(self.access_token, endpoint='/users/@me/workouts')
        self.assertIs(data['meta']['code'], 200)
        self.assertIs(data_generic['meta']['code'], 200)
        self.assertIsNotNone(data['data'])
        self.assertIsNotNone(data_generic['data'])

    def test_get_trends(self):
        data = self.j.get_trends(self.access_token)
        data_generic = self.j.get_generic_api_call(self.access_token, endpoint='/users/@me/trends')
        self.assertIs(data['meta']['code'], 200)
        self.assertIs(data_generic['meta']['code'], 200)
        self.assertIsNotNone(data['data'])
        self.assertIsNotNone(data_generic['data'])

    def test_get_sleeps_list(self):
        data = self.j.get_sleeps_list(self.access_token)
        data_generic = self.j.get_generic_api_call(self.access_token, endpoint='/users/@me/sleeps')
        self.assertIs(data['meta']['code'], 200)
        self.assertIs(data_generic['meta']['code'], 200)
        self.assertIsNotNone(data['data'])
        self.assertIsNotNone(data_generic['data'])

    def test_get_moves_list(self):git 
        data = self.j.get_moves_list(self.access_token)
        data_generic = self.j.get_generic_api_call(self.access_token, endpoint='/users/@me/moves')
        self.assertIs(data['meta']['code'], 200)
        self.assertIs(data_generic['meta']['code'], 200)
        self.assertIsNotNone(data['data'])
        self.assertIsNotNone(data_generic['data'])



if __name__ == '__main__':
    unittest.main()
