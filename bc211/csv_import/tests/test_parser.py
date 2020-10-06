import logging
from django.test import TestCase
from common.testhelpers.random_test_values import a_string, an_email_address
from ..parser import parse
from .helpers import Bc211CsvDataBuilder

logging.disable(logging.ERROR)

ORGANIZATION_ID_HEADER = 'ResourceAgencyNum'
ORGANIZATION_NAME_HEADER = 'PublicName'
ORGANIZATION_DESCRIPTION = 'AgencyDescription'


class ParserTests(TestCase):
    def test_can_parse_organization_id(self):
        the_id = a_string()
        data = Bc211CsvDataBuilder().with_field(ORGANIZATION_ID_HEADER, the_id).build()
        parsed_data = parse(data)
        self.assertEqual(parsed_data[0]['id'], the_id)

    def test_can_parse_organization_name(self):
        the_name = a_string()
        data = Bc211CsvDataBuilder().with_field(ORGANIZATION_NAME_HEADER, the_name).build()
        parsed_data = parse(data)
        self.assertEqual(parsed_data[0]['name'], the_name)

    def test_can_parse_organization_alternate_name(self):
        the_name = a_string()
        data = Bc211CsvDataBuilder().with_field('AlternateName', the_name).build()
        parsed_data = parse(data)
        self.assertEqual(parsed_data[0]['alternate_name'], the_name)

    def test_can_parse_description(self):
        the_description = a_string()
        data = Bc211CsvDataBuilder().with_field(ORGANIZATION_DESCRIPTION, the_description).build()
        parsed_data = parse(data)
        self.assertEqual(parsed_data[0]['description'], the_description)

    # email url
    def test_can_parse_email(self):
        the_email = an_email_address()
        data = Bc211CsvDataBuilder().with_field('EmailAddressMain', the_email).build()
        parsed_data = parse(data)
        self.assertEqual(parsed_data[0]['email'], the_email)

    def test_can_parse_two_organizations(self):
        first_name = a_string()
        second_name = a_string()
        data = (Bc211CsvDataBuilder().
                with_field(ORGANIZATION_NAME_HEADER, first_name).next_row().
                with_field(ORGANIZATION_NAME_HEADER, second_name).build())
        parsed_data = parse(data)
        self.assertEqual(parsed_data[0]['name'], first_name)
        self.assertEqual(parsed_data[1]['name'], second_name)
