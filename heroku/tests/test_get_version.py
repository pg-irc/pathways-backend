from django.test import TestCase
from heroku import version
from yaml import safe_load

class TestVersion(TestCase):

    def setUp(self):
        with open('runtime.txt', 'r') as file:
            self.version = file.read().strip()

    def test_version_in_heroku_init_py_matches_runtime_txt(self):
        version_string = version.get_python_runtime_version_string()
        self.assertEqual(version_string, self.version)

    def test_version_in_heroku_init_py_matches_travis_yml(self):
        with open('.travis.yml', 'r') as stream:
            travis_configuration_data = safe_load(stream)
            travis_python_version = travis_configuration_data['python']
            prefixed_travis_python_version = 'python-{}'.format(travis_python_version)
            self.assertEqual(prefixed_travis_python_version, self.version)
