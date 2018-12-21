from django.test import TestCase
from rest_framework import status
from main import version


class TestVersion(TestCase):

    def setUp(self):
        with open('VERSION.txt', 'r') as file:
            self.version = file.read().strip()

    def test_get_version_string_matches_version_dot_txt(self):
        version_string = version.get_version_string()
        self.assertEqual(version_string, self.version)

    def test_get_version_info_matches_version_dot_txt(self):
        version_tuple = version.get_version_info()
        version_string = '{}.{}.{}'.format(version_tuple[0], version_tuple[1], version_tuple[2])
        self.assertEqual(version_string, self.version)

    def test_get_version_from_api(self):
        url = '/version/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content.decode("utf-8"), self.version)
