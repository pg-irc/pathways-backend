import types
from django.test import TestCase
from rest_framework.exceptions import ParseError
from common.filter_parameter_parsers import ProximityParameterParser

class ProximityParameterParserTests(TestCase):

    def test_parses_proximity_with_white_space(self):
        proximity = ProximityParameterParser(' 1.1111, 22.2222    ').parse()
        self.assertEqual(proximity[0], 1.1111)
        self.assertEqual(proximity[1], 22.2222)

    def test_throws_when_proximity_has_less_than_two_values(self):
        with self.assertRaisesRegex(ParseError, ProximityParameterParser.errors['exactly_two_values']):
            ProximityParameterParser('1.1111').parse()

    def test_throws_when_proximity_has_more_than_two_values(self):
        with self.assertRaisesRegex(ParseError, ProximityParameterParser.errors['exactly_two_values']):
            ProximityParameterParser('1.1111,22.2222,33.3333').parse()

    def test_throws_when_proximity_uses_non_comma_separator(self):
        with self.assertRaisesRegex(ParseError, ProximityParameterParser.errors['exactly_two_values']):
            ProximityParameterParser('1.1111&22.2222&333.3333').parse()

    def test_throws_when_first_proximity_value_cannot_be_parsed_to_latitude(self):
        with self.assertRaisesRegex(ParseError, ProximityParameterParser.errors['invalid_latitude_value_type']):
            ProximityParameterParser('foo,1.1111').parse()

    def test_throws_when_second_proximity_value_cannot_be_parsed_to_longitude(self):
        with self.assertRaisesRegex(ParseError, ProximityParameterParser.errors['invalid_longitude_value_type']):
            ProximityParameterParser('1.1111,foo').parse()
