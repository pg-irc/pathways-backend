import unittest
import string
from django.test import TestCase
from .helpers import (OpenReferralCsvOrganizationBuilder, OpenReferralCsvServiceBuilder,
                        OpenReferralCsvLocationBuilder, OpenReferralCsvServiceAtLocationBuilder, OpenReferralCsvAddressBuilder)
from ..organization import parse_organization
from ..service import parse_service
from ..location import parse_location
from ..service_at_location import parse_service_at_location
from ..address import parse_address
from ..parser import parse_required_field, parse_optional_field, parse_website_with_prefix, parse_coordinate_if_defined, parse_organization_id
from common.testhelpers.random_test_values import (a_string, an_email_address, a_website_address,
                                                    a_latitude_as_a_string, a_longitude_as_a_string)
from human_services.organizations.tests.helpers import OrganizationBuilder
from human_services.services.tests.helpers import ServiceBuilder
from human_services.locations.tests.helpers import LocationBuilder


class OpenReferralOrganizationParserTests(TestCase):
    def test_can_parse_id(self):
        the_id = a_string()
        parsed_organization_id = parse_organization_id(the_id)
        self.assertEqual(parsed_organization_id, the_id)
    
    def test_can_parse_name(self):
        the_name = a_string()
        organization_data = OpenReferralCsvOrganizationBuilder().with_name(the_name).build()
        organization = parse_organization(organization_data)
        self.assertEqual(organization['name'], the_name)

    def test_can_parse_alternate_name(self):
        the_alternate_name = a_string()
        organization_data = OpenReferralCsvOrganizationBuilder().with_alternate_name(the_alternate_name).build()
        organization = parse_organization(organization_data)
        self.assertEqual(organization['alternate_name'], the_alternate_name)
    
    def test_can_parse_description(self):
        the_description = a_string()
        organization_data = OpenReferralCsvOrganizationBuilder().with_description(the_description).build()
        organization = parse_organization(organization_data)
        self.assertEqual(organization['description'], the_description)

    def test_can_parse_email(self):
        the_email = an_email_address()
        organization_data = OpenReferralCsvOrganizationBuilder().with_email(the_email).build()
        organization = parse_organization(organization_data)
        self.assertEqual(organization['email'], the_email)

    def test_can_parse_website(self):
        the_website = a_website_address()
        organization_data = OpenReferralCsvOrganizationBuilder().with_url(the_website).build()
        organization = parse_organization(organization_data)
        self.assertEqual(organization['website'], the_website)


class OpenReferralServiceParserTests(TestCase):
    def setUp(self):
        self.headers = ['id', 'organization_id', 'program_id', 'name', 'alternate_name', 'description', 'url', 'email',
                        'status', 'interpretation_services', 'application_process', 'wait_time', 'fees', 'accreditations',
                        'licenses', 'taxonomy_ids']
        self.organization_id_passed_to_organization_builder = a_string()
        self.organization = OrganizationBuilder().with_id(self.organization_id_passed_to_organization_builder).build()

    def test_can_parse_id(self):
        the_id = a_string()
        service_data = OpenReferralCsvServiceBuilder(self.organization).with_id(the_id).build()
        service = parse_service(self.headers, service_data)
        self.assertEqual(service.id, the_id)
    
    def test_can_parse_organization_id(self):
        service_data = OpenReferralCsvServiceBuilder(self.organization).build()
        service = parse_service(self.headers, service_data)
        self.assertEqual(service.organization_id, self.organization_id_passed_to_organization_builder)
    
    def test_can_parse_name(self):
        the_name = a_string()
        service_data = OpenReferralCsvServiceBuilder(self.organization).with_name(the_name).build()
        service = parse_service(self.headers, service_data)
        self.assertEqual = (service.name, the_name)

    def test_can_parse_alternate_name(self):
        the_alternate_name = a_string()
        service_data = OpenReferralCsvServiceBuilder(self.organization).with_alternate_name(the_alternate_name).build()
        service = parse_service(self.headers, service_data)
        self.assertEqual(service.alternate_name, the_alternate_name)

    def test_can_parse_description(self):
        the_description = a_string()
        service_data = OpenReferralCsvServiceBuilder(self.organization).with_description(the_description).build()
        service = parse_service(self.headers, service_data)
        self.assertEqual(service.description, the_description)

    def test_can_parse_website(self):
        the_website = a_website_address()
        service_data = OpenReferralCsvServiceBuilder(self.organization).with_url(the_website).build()
        service = parse_service(self.headers, service_data)
        self.assertEqual(service.website, the_website)

    def test_can_parse_email(self):
        the_email = an_email_address()
        service_data = OpenReferralCsvServiceBuilder(self.organization).with_email(the_email).build()
        service = parse_service(self.headers, service_data)
        self.assertEqual(service.email, the_email)


class OpenReferralLocationParserTests(TestCase):
    def setUp(self):
        self.headers = ['id', 'organization_id', 'name', 'alternate_name', 'description', 'transportation',
                        'latitude', 'longitude']
        self.organization_id_passed_to_organization_builder = a_string()
        self.organization = OrganizationBuilder().with_id(self.organization_id_passed_to_organization_builder).build()

    def test_can_parse_id(self):
        the_id = a_string()
        location_data = OpenReferralCsvLocationBuilder(self.organization).with_id(the_id).build()
        location = parse_location(self.headers, location_data)
        self.assertEqual(location.id, the_id)
    
    def test_can_parse_organization_id(self):
        location_data = OpenReferralCsvLocationBuilder(self.organization).build()
        location = parse_location(self.headers, location_data)
        self.assertEqual(location.organization_id, self.organization_id_passed_to_organization_builder)
    
    def test_can_parse_name(self):
        the_name = a_string()
        location_data = OpenReferralCsvLocationBuilder(self.organization).with_name(the_name).build()
        location = parse_location(self.headers, location_data)
        self.assertEqual(location.name, the_name)
    
    def test_can_parse_alternate_name(self):
        the_alternate_name = a_string()
        location_data = OpenReferralCsvLocationBuilder(self.organization).with_alternate_name(the_alternate_name).build()
        location = parse_location(self.headers, location_data)
        self.assertEqual(location.alternate_name, the_alternate_name)
    
    def test_can_parse_description(self):
        the_description = a_string()
        location_data = OpenReferralCsvLocationBuilder(self.organization).with_description(the_description).build()
        location = parse_location(self.headers, location_data)
        self.assertEqual(location.description, the_description)

    def test_can_parse_latitude(self):
        the_latitude = a_latitude_as_a_string()
        location_data = OpenReferralCsvLocationBuilder(self.organization).with_latitude(the_latitude).build()
        location = parse_location(self.headers, location_data)
        self.assertEqual(location.spatial_location.latitude, float(the_latitude))

    def test_can_parse_longitude(self):
        the_longitude = a_longitude_as_a_string()
        location_data = OpenReferralCsvLocationBuilder(self.organization).with_longitude(the_longitude).build()
        location = parse_location(self.headers, location_data)
        self.assertEqual(location.spatial_location.longitude, float(the_longitude))



class OpenReferralServicesAtLocationParserTests(TestCase):
    def setUp(self):
        self.headers = ['id', 'service_id', 'location_id', 'description']
        organization = OrganizationBuilder().build()
        self.service_id_passed_to_service_builder = a_string()
        self.location_id_passed_to_location_builder = a_string()
        self.service = ServiceBuilder(organization).with_id(self.service_id_passed_to_service_builder).build()
        self.location = LocationBuilder(organization).with_id(self.location_id_passed_to_location_builder).build()
    
    def test_can_parse_service_id(self):
        service_at_location_data = OpenReferralCsvServiceAtLocationBuilder(self.service, self.location).build()
        service_at_location = parse_service_at_location(self.headers, service_at_location_data)
        self.assertEqual(service_at_location.service_id, self.service_id_passed_to_service_builder)
    
    def test_can_parse_location_id(self):
        service_at_location_data = OpenReferralCsvServiceAtLocationBuilder(self.service, self.location).build()
        service_at_location = parse_service_at_location(self.headers, service_at_location_data)
        self.assertEqual(service_at_location.location_id, self.location_id_passed_to_location_builder)


class OpenReferralAddressesParserTests(TestCase):
    def setUp(self):
        self.headers = ['id', 'type', 'location_id', 'attention', 'address_1', 'address_2', 'address_3', 'address_4', 'city',
                        'region', 'state_province', 'postal_code', 'country']
        organization = OrganizationBuilder().build()
        self.location_id_passed_to_location_builder = a_string()
        self.location = LocationBuilder(organization).with_id(self.location_id_passed_to_location_builder).build()
    
    def test_can_parse_type(self):
        the_type = 'postal_address'
        address_data = OpenReferralCsvAddressBuilder(self.location).with_address_type(the_type).build()
        address = parse_address(self.headers, address_data)
        self.assertEqual(address.type, the_type)

    def test_can_parse_location_id(self):
        address_data = OpenReferralCsvAddressBuilder(self.location).build()
        address = parse_address(self.headers, address_data)
        self.assertEqual(address.location_id, self.location_id_passed_to_location_builder)

    def test_can_parse_attention(self):
        the_attention = a_string()
        address_data = OpenReferralCsvAddressBuilder(self.location).with_attention(the_attention).build()
        address = parse_address(self.headers, address_data)
        self.assertEqual(address.attention, the_attention)
    
    def test_can_parse_address(self):
        the_address = a_string()
        address_data = OpenReferralCsvAddressBuilder(self.location).with_address(the_address).build()
        address = parse_address(self.headers, address_data)
        self.assertEqual(address.address, the_address)
    
    def test_can_parse_city(self):
        the_city = a_string()
        address_data = OpenReferralCsvAddressBuilder(self.location).with_city(the_city).build()
        address = parse_address(self.headers, address_data)
        self.assertEqual(address.city, the_city)
    
    def test_can_parse_state_province(self):
        the_state_province = a_string()
        address_data = OpenReferralCsvAddressBuilder(self.location).with_state_province(the_state_province).build()
        address = parse_address(self.headers, address_data)
        self.assertEqual(address.state_province, the_state_province)

    def test_can_parse_postal_code(self):
        the_postal_code = a_string()
        address_data = OpenReferralCsvAddressBuilder(self.location).with_postal_code(the_postal_code).build()
        address = parse_address(self.headers, address_data)
        self.assertEqual(address.postal_code, the_postal_code)
    
    def test_can_parse_country(self):
        the_country = a_string(2, string.ascii_uppercase)
        address_data = OpenReferralCsvAddressBuilder(self.location).with_country(the_country).build()
        address = parse_address(self.headers, address_data)
        self.assertEqual(address.country, the_country)


class ParserHelperTests(TestCase):
    def test_removes_doubly_escaped_bold_markup_from_optional_field(self):
        the_alternate_name = '&amp;lt;b&amp;gt;abc'
        html_markup = parse_optional_field('alternate_name', the_alternate_name)
        self.assertEqual(html_markup, 'abc')

    def test_removes_doubly_escaped_strong_markup_from_optional_field(self):
        the_alternate_name = '&amp;lt;strong&amp;gt;abc'
        html_markup = parse_optional_field('alternate_name', the_alternate_name)
        self.assertEqual(html_markup, 'abc')

    def test_website_without_prefix_parsed_as_http(self):
        the_website = 'www.example.org'
        parsed_website = parse_website_with_prefix('website', the_website)
        self.assertEqual(parsed_website, 'http://www.example.org')

    def test_website_with_http_prefix_parsed_as_http(self):
        the_website = 'http://www.example.org'
        parsed_website = parse_website_with_prefix('website', the_website)
        self.assertEqual(parsed_website, 'http://www.example.org')

    def test_website_with_https_prefix_parsed_as_https(self):
        the_website = 'https://www.example.org'
        parsed_website = parse_website_with_prefix('website', the_website)
        self.assertEqual(parsed_website, 'https://www.example.org')
    
    def test_returns_none_if_coordinate_is_empty(self):
        empty_latitude = ''
        foo = parse_coordinate_if_defined('latitude', empty_latitude)
        self.assertEqual(foo, None)
