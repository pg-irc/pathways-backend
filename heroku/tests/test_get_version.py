from django.test import TestCase
from heroku import version


class TestVersion(TestCase):

    def setUp(self):
        with open('runtime.txt', 'r') as file:
            self.version = file.read().strip()

    def test_python_runtime_version_string_in_heroku_init_py_matches_runtime_dot_txt(self):
        version_string = version.get_python_runtime_version_string()
        self.assertEqual(version_string, self.version)
