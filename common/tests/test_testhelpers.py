from django.test import TestCase
from common.testhelpers.random_test_values import a_string


class TestTestHelpers(TestCase):
    def setUp(self):
        self.a_string_default = a_string()

    def test_a_string_can_produce_valid_country_code(self):
        a_string_country_code = a_string(2, 'CA')
        possible_country_codes = ['CA', 'AC', 'CC', 'AA']
        return self.assertIn(a_string_country_code, possible_country_codes)

    def test_a_string_by_default_is_20_characters_long(self):
        return self.assertEqual(len(self.a_string_default), 20)

    def test_a_string_by_default_is_alpha(self):
        return self.assertTrue(self.a_string_default.isalpha())
