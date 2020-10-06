import logging
from django.test import TestCase
from common.testhelpers.random_test_values import a_string, a_website_address, an_email_address
from ..parser import parse
from .helpers import Bc211CsvDataBuilder

logging.disable(logging.ERROR)


class ParsingOfOrganizationsTests(TestCase):
    def test_can_parse_organization_id(self):
        the_id = a_string()
        data = Bc211CsvDataBuilder().with_field('ResourceAgencyNum', the_id).build()
        parsed_data = parse(data)
        self.assertEqual(parsed_data[0]['id'], the_id)

    def test_can_parse_organization_name(self):
        the_name = a_string()
        data = Bc211CsvDataBuilder().with_field('PublicName', the_name).build()
        parsed_data = parse(data)
        self.assertEqual(parsed_data[0]['name'], the_name)

    def test_can_parse_organization_alternate_name(self):
        the_name = a_string()
        data = Bc211CsvDataBuilder().with_field('AlternateName', the_name).build()
        parsed_data = parse(data)
        self.assertEqual(parsed_data[0]['alternate_name'], the_name)

    def test_can_parse_description(self):
        the_description = a_string()
        data = Bc211CsvDataBuilder().with_field('AgencyDescription', the_description).build()
        parsed_data = parse(data)
        self.assertEqual(parsed_data[0]['description'], the_description)

    def test_can_parse_email(self):
        the_email = an_email_address()
        data = Bc211CsvDataBuilder().with_field('EmailAddressMain', the_email).build()
        parsed_data = parse(data)
        self.assertEqual(parsed_data[0]['email'], the_email)

    def test_can_parse_url(self):
        the_url = a_website_address()
        data = Bc211CsvDataBuilder().with_field('WebsiteAddress', the_url).build()
        parsed_data = parse(data)
        self.assertEqual(parsed_data[0]['url'], the_url)

    def test_can_parse_two_organizations(self):
        first_name = a_string()
        second_name = a_string()
        data = (Bc211CsvDataBuilder().
                with_field('PublicName', first_name).next_row().
                with_field('PublicName', second_name).build())
        parsed_data = parse(data)
        self.assertEqual(parsed_data[0]['name'], first_name)
        self.assertEqual(parsed_data[1]['name'], second_name)
