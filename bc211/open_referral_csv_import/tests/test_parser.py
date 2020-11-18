import string
from django.test import TestCase
from bc211.open_referral_csv_import.tests.helpers import OpenReferralCsvAddressBuilder
from bc211.open_referral_csv_import import parser
from common.testhelpers.random_test_values import (a_string, an_email_address, a_website_address,
                                                    a_latitude_as_a_string, a_longitude_as_a_string)
from human_services.organizations.tests.helpers import OrganizationBuilder
from human_services.services.tests.helpers import ServiceBuilder
from human_services.locations.tests.helpers import LocationBuilder
from bc211.parser import remove_double_escaped_html_markup
from bc211.open_referral_csv_import.exceptions import MissingRequiredFieldCsvParseException


class OpenReferralLocationParserTests(TestCase):
    def test_can_parse_latitude(self):
        the_latitude = a_latitude_as_a_string()
        parsed_latitude = parser.parse_coordinate_if_defined(the_latitude)
        self.assertEqual(parsed_latitude, float(the_latitude))

    def test_can_parse_longitude(self):
        the_longitude = a_longitude_as_a_string()
        parsed_longitude = parser.parse_coordinate_if_defined(the_longitude)
        self.assertEqual(parsed_longitude, float(the_longitude))


class ParserHelperTests(TestCase):
    def test_removes_doubly_escaped_bold_markup_from_field(self):
        the_name = '&amp;lt;b&amp;gt;abc'
        html_markup = remove_double_escaped_html_markup(the_name)
        self.assertEqual(html_markup, 'abc')

    def test_removes_doubly_escaped_strong_markup_from_field(self):
        the_name = '&amp;lt;strong&amp;gt;abc'
        html_markup = remove_double_escaped_html_markup(the_name)
        self.assertEqual(html_markup, 'abc')

    def test_throws_when_required_field_is_missing(self):
        with self.assertRaises(MissingRequiredFieldCsvParseException):
            parser.parse_required_field('id', None)

    def test_returns_empty_string_if_optional_field_is_missing(self):
        parsed_id = parser.parse_optional_field(None)
        self.assertEqual(parsed_id, '')

    def test_website_without_prefix_parsed_as_http(self):
        the_website = 'www.example.org'
        parsed_website = parser.parse_website_with_prefix(a_string(), the_website)
        self.assertEqual(parsed_website, 'http://www.example.org')

    def test_website_with_http_prefix_parsed_as_http(self):
        the_website = 'http://www.example.org'
        parsed_website = parser.parse_website_with_prefix(a_string(), the_website)
        self.assertEqual(parsed_website, 'http://www.example.org')

    def test_website_with_https_prefix_parsed_as_https(self):
        the_website = 'https://www.example.org'
        parsed_website = parser.parse_website_with_prefix(a_string(), the_website)
        self.assertEqual(parsed_website, 'https://www.example.org')

    def test_returns_none_if_coordinate_is_empty(self):
        empty_latitude = ''
        foo = parser.parse_coordinate_if_defined(empty_latitude)
        self.assertEqual(foo, None)

    def test_invalid_email_returns_None(self):
        the_email = 'vancouver@ami.ca?'
        parsed_email = parser.parse_email(a_string(), the_email)
        self.assertEqual(parsed_email, None)

    def test_invalid_website_returns_None(self):
        the_website = 'httpL//(none)'
        parsed_website = parser.parse_website_with_prefix(a_string(), the_website)
        self.assertEqual(parsed_website, None)