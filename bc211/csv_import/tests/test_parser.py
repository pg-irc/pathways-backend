import logging
import hashlib
from django.test import TestCase
from common.testhelpers.random_test_values import a_float, a_latitude, a_longitude, a_phone_number, a_string, a_website_address, an_email_address, an_integer
from bc211.csv_import.tests.helpers import Bc211CsvDataBuilder
from bc211.csv_import.parser import compute_hash, parse, phone_header_with_index_one

logging.disable(logging.ERROR)


class TestDataSink:
    def __init__(self):
        self.organizations = []
        self.services = []
        self.locations = []
        self.services_at_location = []
        self.addresses = []
        self.phone_numbers = []

    def write_organization(self, organization):
        self.organizations.append(organization)

    def write_service(self, service, location_id):
        self.services.append(service)
        the_id = compute_hash(service['id'], location_id)
        self.services_at_location.append({'id': the_id, 'service_id': service['id'], 'location_id': location_id})

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

    def services_at_location(self):
        return self.services_at_location

    def first_location(self):
        return self.locations[0]

    def first_address(self):
        return self.addresses[0]

    def second_address(self):
        return self.addresses[1]

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
        the_alternate_name = a_string()
        data = Bc211CsvDataBuilder().as_organization().with_field('AlternateName', the_alternate_name).build()
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.first_organization()['alternate_name'], the_alternate_name)

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

    def test_sets_location_id_on_phone_number_record_for_organization(self):
        the_number = a_phone_number()
        the_name = a_string()
        the_organization_id = a_string()
        data = (Bc211CsvDataBuilder().
                as_organization().
                with_field('ResourceAgencyNum', the_organization_id).
                with_field('PublicName', the_name).
                with_field('Phone1Number', the_number).
                build())
        parsed_data = parse(TestDataSink(), data)
        location_id = compute_hash(the_name)
        self.assertEqual(parsed_data.first_phone_number()['location_id'], location_id)

    def test_sets_location_id_on_phone_number_record_for_service(self):
        the_number = a_phone_number()
        the_name = a_string()
        the_service_id = a_string()
        data = (Bc211CsvDataBuilder().
                as_service().
                with_field('PublicName', the_name).
                with_field('ResourceAgencyNum', the_service_id).
                with_field('Phone1Number', the_number).
                build())
        parsed_data = parse(TestDataSink(), data)
        the_location_id = compute_hash(the_name)
        self.assertEqual(parsed_data.first_phone_number()['location_id'], the_location_id)

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
        the_phone_description = a_string()
        data = (Bc211CsvDataBuilder().
                as_organization().
                with_field('Phone1Name', the_phone_description).
                with_field('Phone1Number', a_phone_number()).
                build())
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.first_phone_number()['description'], the_phone_description)

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
# TODO determine if other address fields are used for any records


class ParseLocationsTests(TestCase):

    def test_parses_organization_name_as_location_name(self):
        the_name = a_string()
        data = (Bc211CsvDataBuilder().
                as_organization().
                with_field('PublicName', the_name).
                build())
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.first_location()['name'], the_name)

    def test_parses_organization_alternate_name_as_location_name(self):
        the_alternate_name = a_string()
        data = (Bc211CsvDataBuilder().
                as_organization().
                with_field('AlternateName', the_alternate_name).
                build())
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.first_location()['alternate_name'], the_alternate_name)

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
        the_longitude = a_longitude()
        data = (Bc211CsvDataBuilder().
                as_organization().
                with_field('Longitude', str(the_longitude)).
                build())
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.first_location()['longitude'], the_longitude)

    # Need the test to show that one service can have >1 locations, and each location can have >1 service


class HumanServiceEntityRelationsTests(TestCase):
    # TODO make this test have only one of each entity, test one-to-many relations in separate tests
    def setUp(self):
        self.the_organization_id = a_string()
        self.the_organization_name = a_string()
        self.the_alternate_name = a_string()
        self.the_description = a_string()
        self.the_email = an_email_address()
        self.the_url = a_website_address()
        self.the_number = a_phone_number()
        self.the_second_number = a_phone_number()
        self.the_type = a_string()
        self.the_phone_description = a_string()
        self.the_latitude = a_latitude()
        self.the_longitude = a_longitude()
        self.the_address_line = a_string()
        self.the_city_line = a_string()
        self.the_province = a_string()
        self.the_postal_code = a_string()
        self.the_country = a_string()
        self.the_first_service_id = a_string()
        self.the_first_service_name = a_string()
        self.the_first_service_address = a_string()
        self.the_first_service_phone_number = a_phone_number()
        self.the_second_service_id = a_string()
        self.the_second_service_name = a_string()
        self.the_second_service_address = a_string()
        self.the_second_service_phone_number = a_phone_number()
        data = (Bc211CsvDataBuilder().
                as_organization().
                with_field('ResourceAgencyNum', self.the_organization_id).
                with_field('PublicName', self.the_organization_name).
                with_field('AlternateName', self.the_alternate_name).
                with_field('AgencyDescription', self.the_description).
                with_field('EmailAddressMain', self.the_email).
                with_field('WebsiteAddress', self.the_url).
                with_field('Phone1Number', self.the_number).
                with_field('Phone1Type', self.the_type).
                with_field('Phone1Name', self.the_phone_description).
                with_field('Phone2Number', self.the_second_number).
                with_field('Latitude', str(self.the_latitude)).
                with_field('Longitude', str(self.the_longitude)).
                with_field('MailingAddress1', self.the_address_line).
                with_field('MailingCity', self.the_city_line).
                with_field('MailingStateProvince', self.the_province).
                with_field('MailingPostalCode', self.the_postal_code).
                with_field('MailingCountry', self.the_country).
                next_row().
                as_service().
                with_field('ResourceAgencyNum', self.the_first_service_id).
                with_field('ParentAgencyNum', self.the_organization_id).
                with_field('PublicName', self.the_first_service_name).
                with_field('MailingAddress1', self.the_first_service_address).
                with_field('Phone1Number', self.the_first_service_phone_number).
                next_row().
                as_service().
                with_field('ResourceAgencyNum', self.the_second_service_id).
                with_field('ParentAgencyNum', self.the_organization_id).
                with_field('PublicName', self.the_second_service_name).
                with_field('MailingAddress1', self.the_second_service_address).
                with_field('Phone1Number', self.the_second_service_phone_number).
                build())
        self.parsed_data = parse(TestDataSink(), data)

    def test_foo(self):
        self.assertEqual(len(self.parsed_data.organizations), 1)
        self.assertEqual(self.parsed_data.first_organization()['id'], self.the_organization_id)
        self.assertEqual(self.parsed_data.first_organization()['name'], self.the_organization_name)
        self.assertEqual(self.parsed_data.first_organization()['alternate_name'], self.the_alternate_name)
        self.assertEqual(self.parsed_data.first_organization()['description'], self.the_description)
        self.assertEqual(self.parsed_data.first_organization()['email'], self.the_email)
        self.assertEqual(self.parsed_data.first_organization()['url'], self.the_url)

        self.assertEqual(len(self.parsed_data.services), 2)
        self.assertEqual(self.parsed_data.first_service()['id'], self.the_first_service_id)
        self.assertEqual(self.parsed_data.services[1]['id'], self.the_second_service_id)

        self.assertEqual(len(self.parsed_data.services_at_location), 2)

        self.assertEqual(len(self.parsed_data.phone_numbers), 4)
        self.assertEqual(self.parsed_data.first_phone_number()['number'], self.the_number)
        self.assertEqual(self.parsed_data.first_phone_number()['location_id'], compute_hash(self.the_organization_name))
        self.assertEqual(self.parsed_data.first_phone_number()['type'], self.the_type)
        self.assertEqual(self.parsed_data.first_phone_number()['description'], self.the_phone_description)
        self.assertEqual(self.parsed_data.phone_numbers[1]['number'], self.the_second_number)

        self.the_location_id_for_now = compute_hash(self.the_organization_name)
        self.assertEqual(len(self.parsed_data.locations), 3)  # TODO this is not right
        self.assertEqual(self.parsed_data.first_location()['id'], self.the_location_id_for_now)
        self.assertEqual(self.parsed_data.first_location()['organization_id'], self.the_organization_id)
        self.assertEqual(self.parsed_data.first_location()['name'], self.the_organization_name)
        self.assertEqual(self.parsed_data.first_location()['alternate_name'], self.the_alternate_name)
        self.assertEqual(self.parsed_data.first_location()['latitude'], self.the_latitude)
        self.assertEqual(self.parsed_data.first_location()['longitude'], self.the_longitude)

        self.assertEqual(len(self.parsed_data.addresses), 6)  # TODO this should be 3
        self.assertEqual(self.parsed_data.first_address()['address_1'], self.the_address_line)
        self.assertEqual(self.parsed_data.first_address()['city'], self.the_city_line)
        self.assertEqual(self.parsed_data.first_address()['state_province'], self.the_province)
        self.assertEqual(self.parsed_data.first_address()['postal_code'], self.the_postal_code)
        self.assertEqual(self.parsed_data.first_address()['country'], self.the_country)

        self.assertEqual(self.parsed_data.services[0]['organization_id'], self.the_organization_id)
        self.assertEqual(self.parsed_data.services[1]['organization_id'], self.the_organization_id)

        self.assertEqual(self.parsed_data.locations[0]['organization_id'], self.the_organization_id)
        self.assertEqual(self.parsed_data.locations[1]['organization_id'], self.the_organization_id)
        self.assertEqual(self.parsed_data.locations[2]['organization_id'], self.the_organization_id)

        self.assertEqual(self.parsed_data.phone_numbers[0]['location_id'], compute_hash(self.the_organization_name))
        self.assertEqual(self.parsed_data.phone_numbers[1]['location_id'], compute_hash(self.the_organization_name))
        self.assertEqual(self.parsed_data.phone_numbers[2]['location_id'], compute_hash(self.the_first_service_name))
        self.assertEqual(self.parsed_data.phone_numbers[3]['location_id'], compute_hash(self.the_second_service_name))

        self.assertEqual(self.parsed_data.addresses[0]['location_id'], self.the_location_id_for_now)
        self.assertEqual(self.parsed_data.addresses[1]['location_id'], self.the_location_id_for_now)
        self.the_location_id_for_now = compute_hash(self.the_first_service_name)
        self.assertEqual(self.parsed_data.addresses[2]['location_id'], self.the_location_id_for_now)
        self.assertEqual(self.parsed_data.addresses[3]['location_id'], self.the_location_id_for_now)
        self.the_location_id_for_now = compute_hash(self.the_second_service_name)
        self.assertEqual(self.parsed_data.addresses[4]['location_id'], self.the_location_id_for_now)
        self.assertEqual(self.parsed_data.addresses[5]['location_id'], self.the_location_id_for_now)

        # ids for organizations,
        self.assertEqual(self.parsed_data.first_organization()['id'], self.the_organization_id)
        # locations,
        self.the_location_id_for_now = compute_hash(self.the_organization_name)
        self.assertEqual(self.parsed_data.first_location()['id'], self.the_location_id_for_now)
        # phone numbers,
        self.assertGreater(len(self.parsed_data.first_phone_number()['id']), 0)
        # addresses,
        self.assertGreater(len(self.parsed_data.first_address()['id']), 0)
        # services,
        self.assertEqual(self.parsed_data.first_service()['id'], self.the_first_service_id)
        self.assertEqual(self.parsed_data.services[1]['id'], self.the_second_service_id)
        # service@location
        self.assertGreater(len(self.parsed_data.services_at_location[0]['id']), 0)

        # location -> organization
        self.assertEqual(self.parsed_data.first_location()['organization_id'], self.the_organization_id)
        # phone -> location
        self.assertEqual(self.parsed_data.phone_numbers[0]['location_id'], compute_hash(self.the_organization_name))
        self.assertEqual(self.parsed_data.phone_numbers[1]['location_id'], compute_hash(self.the_organization_name))
        self.assertEqual(self.parsed_data.phone_numbers[2]['location_id'], compute_hash(self.the_first_service_name))
        self.assertEqual(self.parsed_data.phone_numbers[3]['location_id'], compute_hash(self.the_second_service_name))
        # address (both kinds) -> location
        self.assertEqual(self.parsed_data.addresses[0]['location_id'], compute_hash(self.the_organization_name))
        self.assertEqual(self.parsed_data.addresses[1]['location_id'], compute_hash(self.the_organization_name))
        self.assertEqual(self.parsed_data.addresses[2]['location_id'], compute_hash(self.the_first_service_name))
        self.assertEqual(self.parsed_data.addresses[3]['location_id'], compute_hash(self.the_first_service_name))
        self.assertEqual(self.parsed_data.addresses[4]['location_id'], compute_hash(self.the_second_service_name))
        self.assertEqual(self.parsed_data.addresses[5]['location_id'], compute_hash(self.the_second_service_name))
        # service -> organization
        self.assertEqual(self.parsed_data.first_service()['organization_id'], self.the_organization_id)
        self.assertEqual(self.parsed_data.services[1]['organization_id'], self.the_organization_id)
        # service -> location
        # location -> service
        self.assertEqual(self.parsed_data.services_at_location[0]['location_id'], compute_hash(self.the_first_service_name))
        self.assertEqual(self.parsed_data.services_at_location[0]['service_id'], self.the_first_service_id)
        self.assertEqual(self.parsed_data.services_at_location[1]['location_id'], compute_hash(self.the_second_service_name))
        self.assertEqual(self.parsed_data.services_at_location[1]['service_id'], self.the_second_service_id)


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
        the_city_line = a_string()
        data = (Bc211CsvDataBuilder().
                as_organization().
                with_field('MailingCity', the_city_line).
                build())
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.first_address()['city'], the_city_line)

    def test_can_parse_address_state_province(self):
        the_province = a_string()
        data = (Bc211CsvDataBuilder().
                as_organization().
                with_field('MailingStateProvince', the_province).
                build())
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.first_address()['state_province'], the_province)

    def test_can_parse_address_postal_code(self):
        the_postal_code = a_string()
        data = (Bc211CsvDataBuilder().
                as_organization().
                with_field('MailingPostalCode', the_postal_code).
                build())
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.first_address()['postal_code'], the_postal_code)

    def test_can_parse_address_country(self):
        the_country = a_string()
        data = (Bc211CsvDataBuilder().
                as_organization().
                with_field('MailingCountry', the_country).
                build())
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.first_address()['country'], the_country)

    def test_can_parse_physical_address(self):
        the_address_line = a_string()
        data = (Bc211CsvDataBuilder().
                as_organization().
                with_field('PhysicalAddress1', the_address_line).
                build())
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.second_address()['address_1'], the_address_line)

    def test_marks_physical_address_as_physical(self):
        data = (Bc211CsvDataBuilder().
                as_organization().
                with_field('PhysicalAddress1', a_string()).
                build())
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.second_address()['type'], 'physical_address')

    def test_marks_postal_address_as_postal(self):
        data = (Bc211CsvDataBuilder().
                as_organization().
                with_field('MailingAddress1', a_string()).
                build())
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.first_address()['type'], 'postal_address')

    def test_can_parse_both_physical_and_postal_address(self):
        the_physical_address_line = a_string()
        the_postal_address_line = a_string()
        data = (Bc211CsvDataBuilder().
                as_organization().
                with_field('MailingAddress1', the_postal_address_line).
                with_field('PhysicalAddress1', the_physical_address_line).
                build())
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(parsed_data.first_address()['address_1'], the_postal_address_line)
        self.assertEqual(parsed_data.second_address()['address_1'], the_physical_address_line)
