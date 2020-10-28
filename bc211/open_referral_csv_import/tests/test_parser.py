import unittest
from django.test import TestCase
from .helpers import OpenReferralCsvOrganizationBuilder, OpenReferralCsvServiceBuilder, OpenReferralCsvLocationBuilder
from ..organization import parse_organization
from ..service import parse_service
from ..location import parse_location
from ..parser import parse_required_field, parse_optional_field, parse_website_with_prefix
from common.testhelpers.random_test_values import a_string, an_email_address, a_website_address
from human_services.organizations.tests.helpers import OrganizationBuilder


class OpenReferralOrganizationParserTests(TestCase):
    def setUp(self):
        self.headers = ['id', 'name', 'alternate_name', 'description', 'email', 'url',
                        'tax_status', 'tax_id', 'year_incorporated', 'legal_status']

    def test_can_parse_id(self):
        the_id = a_string()
        organization_data = OpenReferralCsvOrganizationBuilder().with_id(the_id).build()
        organization = parse_organization(self.headers, organization_data)
        self.assertEqual(organization.id, the_id)
    
    def test_can_parse_name(self):
        the_name = a_string()
        organization_data = OpenReferralCsvOrganizationBuilder().with_name(the_name).build()
        organization = parse_organization(self.headers, organization_data)
        self.assertEqual(organization.name, the_name)

    def test_can_parse_alternate_name(self):
        the_alternate_name = a_string()
        organization_data = OpenReferralCsvOrganizationBuilder().with_alternate_name(the_alternate_name).build()
        organization = parse_organization(self.headers, organization_data)
        self.assertEqual(organization.alternate_name, the_alternate_name)
    
    def test_can_parse_description(self):
        the_description = a_string()
        organization_data = OpenReferralCsvOrganizationBuilder().with_description(the_description).build()
        organization = parse_organization(self.headers, organization_data)
        self.assertEqual(organization.description, the_description)

    def test_can_parse_email(self):
        the_email = an_email_address()
        organization_data = OpenReferralCsvOrganizationBuilder().with_email(the_email).build()
        organization = parse_organization(self.headers, organization_data)
        self.assertEqual(organization.email, the_email)

    def test_can_parse_website(self):
        the_website = a_website_address()
        organization_data = OpenReferralCsvOrganizationBuilder().with_url(the_website).build()
        organization = parse_organization(self.headers, organization_data)
        self.assertEqual(organization.website, the_website)

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


class OpenReferralServiceParserTests(TestCase):
    def setUp(self):
        self.headers = ['id', 'organization_id', 'program_id', 'name', 'alternate_name', 'description', 'url', 'email',
                        'status', 'interpretation_services', 'application_process', 'wait_time', 'fees', 'accreditations',
                        'licenses', 'taxonomy_ids']
        self.organization_id_passed_to_parser = a_string()
        self.organization = OrganizationBuilder().with_id(self.organization_id_passed_to_parser).build()

    def test_can_parse_id(self):
        the_id = a_string()
        service_data = OpenReferralCsvServiceBuilder(self.organization).with_id(the_id).build()
        service = parse_service(self.headers, service_data)
        self.assertEqual(service.id, the_id)
    
    def test_can_parse_organization_id(self):
        service_data = OpenReferralCsvServiceBuilder(self.organization).build()
        service = parse_service(self.headers, service_data)
        self.assertEqual(service.organization_id, self.organization_id_passed_to_parser)
    
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
        self.organization_id_passed_to_parser = a_string()
        self.organization = OrganizationBuilder().with_id(self.organization_id_passed_to_parser).build()

    def test_can_parse_id(self):
        the_id = a_string()
        location_data = OpenReferralCsvLocationBuilder(self.organization).with_id(the_id).build()
        location = parse_location(self.headers, location_data)
        self.assertEqual(location['id'], the_id)
    
    def test_can_parse_organization_id(self):
        location_data = OpenReferralCsvLocationBuilder(self.organization).build()
        location = parse_location(self.headers, location_data)
        self.assertEqual(location['organization_id'], self.organization_id_passed_to_parser)
    
    def test_can_parse_name(self):
        the_name = a_string()
        location_data = OpenReferralCsvLocationBuilder(self.organization).with_name(the_name).build()
        location = parse_location(self.headers, location_data)
        self.assertEqual(location['name'], the_name)
    
    def test_can_parse_alternate_name(self):
        the_alternate_name = a_string()
        location_data = OpenReferralCsvLocationBuilder(self.organization).with_alternate_name(the_alternate_name).build()
        location = parse_location(self.headers, location_data)
        self.assertEqual(location['alternate_name'], the_alternate_name)


class HTMLMarkupParserTests(TestCase):
    def test_removes_doubly_escaped_bold_markup_from_required_field(self):
        the_name = '&amp;lt;b&amp;gt;abc'
        html_markup = parse_required_field('name', the_name)
        self.assertEqual(html_markup, 'abc')

    def test_removes_doubly_escaped_strong_markup_from_required_field(self):
        the_name = '&amp;lt;strong&amp;gt;abc'
        html_markup = parse_required_field('name', the_name)
        self.assertEqual(html_markup, 'abc')

    def test_removes_doubly_escaped_bold_markup_from_optional_field(self):
        the_alternate_name = '&amp;lt;b&amp;gt;abc'
        html_markup = parse_optional_field('alternate_name', the_alternate_name)
        self.assertEqual(html_markup, 'abc')

    def test_removes_doubly_escaped_strong_markup_from_optional_field(self):
        the_alternate_name = '&amp;lt;strong&amp;gt;abc'
        html_markup = parse_optional_field('alternate_name', the_alternate_name)
        self.assertEqual(html_markup, 'abc')