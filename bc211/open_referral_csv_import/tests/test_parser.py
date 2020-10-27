import unittest
from django.test import TestCase
from .helpers import OpenReferralCsvOrganizationBuilder, OpenReferralCsvServiceBuilder
from ..organization import parse_organization
from ..service import parse_service
from ..parser import parse_required_field, parse_optional_field, parse_website_with_prefix
from common.testhelpers.random_test_values import a_string, an_email_address, a_website_address


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

    def test_can_parse_id(self):
        the_id = a_string()
        service_data = OpenReferralCsvServiceBuilder().with_id(the_id).build()
        service = parse_service(self.headers, service_data)
        self.assertEqual(service['id'], the_id)
    
    def test_can_parse_organization_id(self):
        the_organization_id = a_string()
        service_data = OpenReferralCsvServiceBuilder().with_organization_id(the_organization_id).build()
        service = parse_service(self.headers, service_data)
        self.assertEqual(service['organization_id'], the_organization_id)
    
    def test_can_parse_name(self):
        the_name = a_string()
        service_data = OpenReferralCsvServiceBuilder().with_name(the_name).build()
        service = parse_service(self.headers, service_data)
        self.assertEqual = (service['name'], the_name)

    def test_can_parse_alternate_name(self):
        the_alternate_name = a_string()
        service_data = OpenReferralCsvServiceBuilder().with_alternate_name(the_alternate_name).build()
        service = parse_service(self.headers, service_data)
        self.assertEqual(service['alternate_name'], the_alternate_name)

    def test_can_parse_description(self):
        the_description = a_string()
        service_data = OpenReferralCsvServiceBuilder().with_description(the_description).build()
        service = parse_service(self.headers, service_data)
        self.assertEqual(service['description'], the_description)

    def test_can_parse_website(self):
        the_website = a_website_address()
        service_data = OpenReferralCsvServiceBuilder().with_url(the_website).build()
        service = parse_service(self.headers, service_data)
        self.assertEqual(service['website'], the_website)

    def test_can_parse_email(self):
        the_email = an_email_address()
        service_data = OpenReferralCsvServiceBuilder().with_email(the_email).build()
        service = parse_service(self.headers, service_data)
        self.assertEqual(service['email'], the_email)


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