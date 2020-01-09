from django.test import TestCase
from rest_framework import status
from main import version
from yaml import safe_load


class TestVersion(TestCase):

    def setUp(self):
        with open('VERSION.txt', 'r') as file:
            self.version = file.read().strip()

    def test_version_string_in_main_init_py_matches_version_dot_txt(self):
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


class TestPythonVersionConsistency(TestCase):

    def get_travis_runtime_version(self):
        with open('.travis.yml', 'r') as stream:
            travis_configuration_data = safe_load(stream)
            return travis_configuration_data['python']

    def get_heroku_runtime_version(self):
        with open('runtime.txt', 'r') as file:
            return file.read().strip()

    def test_version_in_heroku_init_py_matches_travis_yml(self):
        travis_python_version = self.get_travis_runtime_version()
        prefixed_travis_python_version = 'python-{}'.format(travis_python_version)
        heroku_version = self.get_heroku_runtime_version()
        self.assertEqual(prefixed_travis_python_version, heroku_version)
