from django.test import TestCase
from yaml import safe_load


class TestVersion(TestCase):

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
