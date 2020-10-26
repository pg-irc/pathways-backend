import unittest
from django.test import TestCase
from ..importer import import_organizations_file, parse_organization, parse_required_field, parse_optional_field, parse_website_with_prefix, save_organization
from .helpers import OpenReferralCsvOrganizationBuilder
from common.testhelpers.random_test_values import a_string, an_email_address, a_website_address
from human_services.organizations.models import Organization


class OpenReferralImporterTests(TestCase):
    def test_missing_organizations_file_throws_exception(self):
        incorrect_file_path = '../foo/organizations.csv'
        with self.assertRaises(FileNotFoundError) as error:
            import_organizations_file(incorrect_file_path)


class OpenReferralOrganizationParserTests(TestCase):
    def setUp(self):
        self.headers = ['id', 'name', 'alternate_name', 'description', 'email', 'url']

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


class OpenReferralOrganizationImporterTests(TestCase):
    def setUp(self):
        self.headers = ['id', 'name', 'alternate_name', 'description', 'email', 'url']

    def test_can_import_id(self):
        the_id = a_string()
        organization_data = OpenReferralCsvOrganizationBuilder().with_id(the_id).build()
        organization = parse_organization(self.headers, organization_data)
        save_organization(organization)
        organizations = Organization.objects.all()
        self.assertEqual(organizations[0].id, the_id)
    
    def test_can_import_name(self):
        the_name = a_string()
        organization_data = OpenReferralCsvOrganizationBuilder().with_name(the_name).build()
        organization = parse_organization(self.headers, organization_data)
        save_organization(organization)
        organizations = Organization.objects.all()
        self.assertEqual(organizations[0].name, the_name)

    def test_can_import_alternate_name(self):
        the_alternate_name = a_string()
        organization_data = OpenReferralCsvOrganizationBuilder().with_alternate_name(the_alternate_name).build()
        organization = parse_organization(self.headers, organization_data)
        save_organization(organization)
        organizations = Organization.objects.all()
        self.assertEqual(organizations[0].alternate_name, the_alternate_name)

    def test_can_import_description(self):
        the_description = a_string()
        organization_data = OpenReferralCsvOrganizationBuilder().with_description(the_description).build()
        organization = parse_organization(self.headers, organization_data)
        save_organization(organization)
        organizations = Organization.objects.all()
        self.assertEqual(organizations[0].description, the_description)

    def test_can_import_email(self):
        the_email = an_email_address()
        organization_data = OpenReferralCsvOrganizationBuilder().with_email(the_email).build()
        organization = parse_organization(self.headers, organization_data)
        save_organization(organization)
        organizations = Organization.objects.all()
        self.assertEqual(organizations[0].email, the_email)