import logging
from django.test import TestCase
from common.testhelpers.random_test_values import (a_phone_number, a_string, a_website_address,
                                                   an_email_address, an_integer)
from ..parser import parse
from .helpers import Bc211CsvDataBuilder

logging.disable(logging.ERROR)


class TestDataSink:
    def __init__(self):
        self.organizations = []
        self.phone_numbers = []

    def write_organization(self, organization):
        self.organizations.append(organization)

    def write_phone(self, phone):
        self.phone_numbers.append(phone)

    def organizations(self):
        return self.organizations

    def first_organization(self):
        return self.organizations[0]

    def first_phone_number(self):
        return self.phone_numbers[0]


class ParsinorganizationanizationsTests(TestCase):
    def test_can_parse_organization_id(self):
        the_id = a_string()
        data = Bc211CsvDataBuilder().with_field('ResourceAgencyNum', the_id).build()
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.first_organization()['id'], the_id)

    def test_can_parse_organization_name(self):
        the_name = a_string()
        data = Bc211CsvDataBuilder().with_field('PublicName', the_name).build()
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.first_organization()['name'], the_name)

    def test_can_parse_organization_alternate_name(self):
        the_name = a_string()
        data = Bc211CsvDataBuilder().with_field('AlternateName', the_name).build()
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.first_organization()['alternate_name'], the_name)

    def test_can_parse_description(self):
        the_description = a_string()
        data = Bc211CsvDataBuilder().with_field('AgencyDescription', the_description).build()
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.first_organization()['description'], the_description)

    def test_can_parse_email(self):
        the_email = an_email_address()
        data = Bc211CsvDataBuilder().with_field('EmailAddressMain', the_email).build()
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.first_organization()['email'], the_email)

    def test_can_parse_url(self):
        the_url = a_website_address()
        data = Bc211CsvDataBuilder().with_field('WebsiteAddress', the_url).build()
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.first_organization()['url'], the_url)

    def test_sets_type_to_organization_if_parent_agency_is_zero(self):
        parent_id = '0'
        data = Bc211CsvDataBuilder().with_field('ParentAgencyNum', parent_id).build()
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.first_organization()['type'], 'organization')

    def test_sets_type_to_service_if_parent_agency_is_not_zero(self):
        parent_id = str(an_integer(min=1))
        data = Bc211CsvDataBuilder().with_field('ParentAgencyNum', parent_id).build()
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.first_organization()['type'], 'service')

    def test_can_parse_two_organizations(self):
        first_name = a_string()
        second_name = a_string()
        data = (Bc211CsvDataBuilder().
                as_organization().with_field('PublicName', first_name).next_row().
                as_organization().with_field('PublicName', second_name).build())
        parsed_data = parse(TestDataSink(), data).organizations
        self.assertEqual(parsed_data[0]['name'], first_name)
        self.assertEqual(parsed_data[1]['name'], second_name)

    def test_can_parse_organization_phone_number(self):
        the_number = a_phone_number()
        data = (Bc211CsvDataBuilder().
                as_organization().
                with_field('Phone1Number', the_number).
                build())
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.first_phone_number()['number'], the_number)

    def test_sets_organization_id_on_phone_number_record(self):
        the_number = a_phone_number()
        the_organization_id = a_string()
        data = (Bc211CsvDataBuilder().
                as_organization().
                with_field('ResourceAgencyNum', the_organization_id).
                with_field('Phone1Number', the_number).
                build())
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.first_phone_number()['organization_id'], the_organization_id)

    def test_can_parse_organization_phone_number_type(self):
        the_type = a_string()
        data = (Bc211CsvDataBuilder().
                as_organization().
                with_field('Phone1Type', the_type).
                build())
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.first_phone_number()['type'], the_type)

    def test_can_parse_organization_phone_number_description(self):
        the_description = a_string()
        data = (Bc211CsvDataBuilder().
                as_organization().
                with_field('Phone1Name', the_description).
                build())
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.first_phone_number()['description'], the_description)

    def test_can_parse_second_phone_number(self):
        the_number = a_phone_number()
        fieldname = 'Phone' + str(an_integer(min=2, max=5)) + 'Number'
        data = (Bc211CsvDataBuilder().
                as_organization().
                with_field(fieldname, the_number).
                build())
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.first_phone_number()['number'], the_number)
