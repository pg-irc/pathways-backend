from django.test import TestCase
from heroku import version
import yaml


class TestVersion(TestCase):

    def setUp(self):
        with open('runtime.txt', 'r') as file:
            self.version = file.read().strip()

    def test_python_runtime_version_string_in_heroku_init_py_matches_runtime_dot_txt(self):
        version_string = version.get_python_runtime_version_string()
        self.assertEqual(version_string, self.version)

    def test_python_runtime_version_string_in_heroku_init_py_matches_travis_dot_yml(self):
        with open('.travis.yml', 'r') as stream:
            travis_configuration_data = yaml.safe_load(stream)
            travis_python_version = travis_configuration_data['python']
            formatted_travis_python_version = 'python-{}'.format(travis_python_version)
            self.assertEqual(formatted_travis_python_version, self.version)
