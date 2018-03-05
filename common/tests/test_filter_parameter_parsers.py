from django.test import TestCase
from rest_framework.exceptions import ParseError
from common.filter_parameter_parsers import ProximityParser, TaxonomyParser

class ProximityParserTests(TestCase):
    def test_parses_proximity_with_white_space(self):
        proximity = ProximityParser(' 1.1111, 22.2222    ')
        self.assertEqual(proximity.latitude, 1.1111)
        self.assertEqual(proximity.longitude, 22.2222)

    def test_throws_when_proximity_has_less_than_two_values(self):
        with self.assertRaises(ParseError):
            ProximityParser('1.1111')

    def test_throws_when_proximity_has_more_than_two_values(self):
        with self.assertRaises(ParseError):
            ProximityParser('1.1111,22.2222,33.3333')

    def test_throws_when_proximity_uses_non_comma_separator(self):
        with self.assertRaises(ParseError):
            ProximityParser('1.1111&22.2222&333.3333')

    def test_throws_when_first_proximity_value_cannot_be_parsed_to_latitude(self):
        with self.assertRaises(ParseError):
            ProximityParser('foo,1.1111')

    def test_throws_when_second_proximity_value_cannot_be_parsed_to_longitude(self):
        with self.assertRaises(ParseError):
            ProximityParser('1.1111,foo')


class TaxonomyParserTests(TestCase):
    def test_throws_when_too_many_field_separators(self):
        with self.assertRaises(ParseError):
            TaxonomyParser('foo.bar.baz')

    def test_throws_when_missing_field_separators(self):
        with self.assertRaises(ParseError):
            TaxonomyParser('foobar')

    def test_throws_when_missing_taxonomy_id(self):
        with self.assertRaises(ParseError):
            TaxonomyParser('.bar')

    def test_throws_when_missing_taxonomy_term(self):
        with self.assertRaises(ParseError):
            TaxonomyParser('foo.')
