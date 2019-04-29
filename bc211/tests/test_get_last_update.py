from django.test import TestCase
from rest_framework import status
from bc211 import last_update


class TestLastUpdate(TestCase):

    def setUp(self):
        with open('BC211_LAST_UPDATE.txt', 'r') as file:
            self.last_update = file.read().strip()

    def test_last_update_string_in_bc211_init_py_matches_bc211_last_update_dot_txt(self):
        last_update_string = last_update.get_last_update_string()
        self.assertEqual(last_update_string, self.last_update)

    def test_get_version_from_api(self):
        url = '/dbversion/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content.decode("utf-8"), self.last_update)