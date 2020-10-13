import logging
from django.test import TestCase
from common.testhelpers.random_test_values import a_latitude, a_phone_number, a_string, a_website_address, an_email_address, an_integer
from bc211.csv_import.tests.helpers import Bc211CsvDataBuilder
from bc211.csv_import.parser import phone_header_with_index_one, parse

logging.disable(logging.ERROR)


class TestDataSink:
    def __init__(self):
        self.organizations = []
        self.services = []
        self.locations = []
        self.addresses = []
        self.phone_numbers = []

    def write_organization(self, organization):
        self.organizations.append(organization)

    def write_service(self, service):
        self.services.append(service)

    def write_location(self, location):
        self.locations.append(location)
        return self

    def write_addresses(self, addresses):
        self.addresses += addresses
        return self

    def write_phone_numbers(self, phone_numbers):
        self.phone_numbers += phone_numbers

    def organizations(self):
        return self.organizations

    def first_organization(self):
        return self.organizations[0]

    def services(self):
        return self.services

    def first_service(self):
        return self.services[0]

    def first_location(self):
        return self.locations[0]

    def first_address(self):
        return self.addresses[0]

    def phone_numbers(self):
        return self.phone_numbers

    def first_phone_number(self):
        return self.phone_numbers[0]


class ParseOrganizationsTests(TestCase):
    def test_can_parse_organization_id(self):
        the_id = a_string()
        data = Bc211CsvDataBuilder().as_organization().with_field('ResourceAgencyNum', the_id).build()
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.first_organization()['id'], the_id)

    def test_can_parse_organization_name(self):
        the_name = a_string()
        data = Bc211CsvDataBuilder().as_organization().with_field('PublicName', the_name).build()
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.first_organization()['name'], the_name)

    def test_can_parse_organization_alternate_name(self):
        the_name = a_string()
        data = Bc211CsvDataBuilder().as_organization().with_field('AlternateName', the_name).build()
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.first_organization()['alternate_name'], the_name)

    def test_can_parse_description(self):
        the_description = a_string()
        data = Bc211CsvDataBuilder().as_organization().with_field('AgencyDescription', the_description).build()
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.first_organization()['description'], the_description)

    def test_can_parse_email(self):
        the_email = an_email_address()
        data = Bc211CsvDataBuilder().as_organization().with_field('EmailAddressMain', the_email).build()
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.first_organization()['email'], the_email)

    def test_can_parse_url(self):
        the_url = a_website_address()
        data = Bc211CsvDataBuilder().as_organization().with_field('WebsiteAddress', the_url).build()
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.first_organization()['url'], the_url)

    def test_parse_as_organization_if_parent_agency_is_zero(self):
        parent_id = '0'
        the_id = str(an_integer(min=1))
        data = (Bc211CsvDataBuilder().
                with_field('ResourceAgencyNum', the_id).
                with_field('ParentAgencyNum', parent_id).
                build())
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.first_organization()['id'], the_id)

    def test_can_parse_two_organizations(self):
        first_name = a_string()
        second_name = a_string()
        data = (Bc211CsvDataBuilder().
                as_organization().with_field('PublicName', first_name).next_row().
                as_organization().with_field('PublicName', second_name).build())
        parsed_data = parse(TestDataSink(), data).organizations
        self.assertEqual(parsed_data[0]['name'], first_name)
        self.assertEqual(parsed_data[1]['name'], second_name)


class ParseServicesTests(TestCase):
    def test_parse_as_service_if_parent_agency_is_not_zero(self):
        parent_id = str(an_integer(min=1))
        the_id = str(an_integer(min=1))
        data = (Bc211CsvDataBuilder().
                with_field('ResourceAgencyNum', the_id).
                with_field('ParentAgencyNum', parent_id).
                build())
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.first_service()['id'], the_id)


class ParsePhoneNumbersTests(TestCase):
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

    def test_sets_service_id_on_phone_number_record(self):
        the_number = a_phone_number()
        the_service_id = a_string()
        data = (Bc211CsvDataBuilder().
                as_service().
                with_field('ResourceAgencyNum', the_service_id).
                with_field('Phone1Number', the_number).
                build())
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.first_phone_number()['service_id'], the_service_id)

    def test_can_parse_organization_phone_number_type(self):
        the_type = a_string()
        data = (Bc211CsvDataBuilder().
                as_organization().
                with_field('Phone1Type', the_type).
                with_field('Phone1Number', a_phone_number()).
                build())
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.first_phone_number()['type'], the_type)

    def test_can_parse_organization_phone_number_description(self):
        the_description = a_string()
        data = (Bc211CsvDataBuilder().
                as_organization().
                with_field('Phone1Name', the_description).
                with_field('Phone1Number', a_phone_number()).
                build())
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.first_phone_number()['description'], the_description)

    def test_set_index_on_phone_number_field_to_one(self):
        self.assertEqual(phone_header_with_index_one('Phone1Number'), 'Phone1Number')
        self.assertEqual(phone_header_with_index_one('Phone2Number'), 'Phone1Number')
        self.assertEqual(phone_header_with_index_one('Phone2Type'), 'Phone1Type')
        self.assertEqual(phone_header_with_index_one('PhoneXNumber'), 'PhoneXNumber')

    def test_can_parse_second_phone_number(self):
        first_number = a_phone_number()
        second_number = a_phone_number()
        data = (Bc211CsvDataBuilder().
                as_organization().
                with_field('Phone1Number', first_number).
                with_field('Phone2Number', second_number).
                build())
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.phone_numbers[0]['number'], first_number)
        self.assertEqual(parsed_data.phone_numbers[1]['number'], second_number)

    def test_leaves_out_phone_numbers_with_no_values(self):
        data = Bc211CsvDataBuilder().as_organization().with_field('Phone1Number', '').build()
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(len(parsed_data.phone_numbers), 0)

# TODO determine if the other kinds of phone numbers contain any data


class ParseLocationsTests(TestCase):

    # organization_id, name, alternate_name, description, transportation, latitude, longitude
    def test_parses_organization_name_as_location_name(self):
        the_name = a_string()
        data = (Bc211CsvDataBuilder().
                as_organization().
                with_field('PublicName', the_name).
                build())
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.first_location()['name'], the_name)

    def test_parses_organization_alternate_name_as_location_name(self):
        the_name = a_string()
        data = (Bc211CsvDataBuilder().
                as_organization().
                with_field('AlternateName', the_name).
                build())
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.first_location()['alternate_name'], the_name)

    def test_sets_organization_id_on_parsed_location(self):
        the_id = a_string()
        data = (Bc211CsvDataBuilder().
                as_organization().
                with_field('ResourceAgencyNum', the_id).
                build())
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.first_location()['organization_id'], the_id)

    def test_parse_location_latitude(self):
        the_latitude = a_latitude()
        data = (Bc211CsvDataBuilder().
                as_organization().
                with_field('Latitude', str(the_latitude)).
                build())
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.first_location()['latitude'], the_latitude)

    def test_parse_location_longitude(self):
        the_longitude = a_latitude()
        data = (Bc211CsvDataBuilder().
                as_organization().
                with_field('Longitude', str(the_longitude)).
                build())
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.first_location()['longitude'], the_longitude)


class ParseAddressTests(TestCase):
    def test_can_parse_address_line_one(self):
        the_address_line = a_string()
        data = (Bc211CsvDataBuilder().
                as_organization().
                with_field('MailingAddress1', the_address_line).
                build())
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.first_address()['address_1'], the_address_line)

    def test_can_parse_remaining_address_lines(self):
        address_line_2 = a_string()
        address_line_3 = a_string()
        address_line_4 = a_string()
        data = (Bc211CsvDataBuilder().
                as_organization().
                with_field('MailingAddress2', address_line_2).
                with_field('MailingAddress3', address_line_3).
                with_field('MailingAddress4', address_line_4).
                build())
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.first_address()['address_2'], address_line_2)
        self.assertEqual(parsed_data.first_address()['address_3'], address_line_3)
        self.assertEqual(parsed_data.first_address()['address_4'], address_line_4)

    def test_can_parse_address_city(self):
        the_address_line = a_string()
        data = (Bc211CsvDataBuilder().
                as_organization().
                with_field('MailingCity', the_address_line).
                build())
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.first_address()['city'], the_address_line)

    def test_can_parse_address_state_province(self):
        the_address_line = a_string()
        data = (Bc211CsvDataBuilder().
                as_organization().
                with_field('MailingStateProvince', the_address_line).
                build())
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.first_address()['state_province'], the_address_line)

    def test_can_parse_address_postal_code(self):
        the_address_line = a_string()
        data = (Bc211CsvDataBuilder().
                as_organization().
                with_field('MailingPostalCode', the_address_line).
                build())
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.first_address()['state_province'], the_address_line)

    def test_can_parse_address_country(self):
        the_address_line = a_string()
        data = (Bc211CsvDataBuilder().
                as_organization().
                with_field('MailingCountry', the_address_line).
                build())
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.first_address()['country'], the_address_line)
