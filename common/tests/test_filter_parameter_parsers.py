import types
from django.test import TestCase
from rest_framework.exceptions import ParseError
from common.filter_parameter_parsers import ProximityParser

class ProximityParserTests(TestCase):

    def test_parses_proximity_with_white_space(self):
        proximity = ProximityParser.parse_proximity(' 1.1111, 22.2222    ')
        self.assertEqual(proximity[0], 1.1111)
        self.assertEqual(proximity[1], 22.2222)

    def test_throws_when_proximity_has_less_than_two_values(self):
        with self.assertRaisesRegex(ParseError, ProximityParser.errors['exactly_two_values']):
            ProximityParser.parse_proximity('1.1111')

    def test_throws_when_proximity_has_more_than_two_values(self):
        with self.assertRaisesRegex(ParseError, ProximityParser.errors['exactly_two_values']):
            ProximityParser.parse_proximity('1.1111,22.2222,33.3333')

    def test_throws_when_proximity_uses_non_comma_separator(self):
        with self.assertRaisesRegex(ParseError, ProximityParser.errors['exactly_two_values']):
            ProximityParser.parse_proximity('1.1111&22.2222&333.3333')

    def test_throws_when_first_proximity_value_cannot_be_parsed_to_float(self):
        with self.assertRaisesRegex(ParseError, ProximityParser.errors['invalid_value_types']):
            ProximityParser.parse_proximity('1.1111,foo')

    def test_throws_when_second_proximity_value_cannot_be_parsed_to_float(self):
        with self.assertRaisesRegex(ParseError, ProximityParser.errors['invalid_value_types']):
            ProximityParser.parse_proximity('foo,1.1111')

    def test_throws_when_both_proximity_values_cannot_be_parsed_to_float(self):
        with self.assertRaisesRegex(ParseError, ProximityParser.errors['invalid_value_types']):
            ProximityParser.parse_proximity('foo,bar')

