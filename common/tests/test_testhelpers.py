from django.test import TestCase
from common.testhelpers.random_test_values import a_string


class TestTestHelpers(TestCase):
    def test_a_string_can_produce_valid_country_code(self):
        a_string_country_code = a_string(2, 'CA')
        possible_country_codes = ['CA', 'AC', 'CC', 'AA']
        return self.assertIn(a_string_country_code, possible_country_codes)

    def test_a_string_by_default_is_20_characters_long(self):
        return self.assertEqual(len(a_string()), 20)

    def test_a_string_by_default_is_alpha(self):
        return self.assertTrue(a_string().isalpha())

    def test_a_string_by_default_is_lower(self):
        return self.assertTrue(a_string().islower())
