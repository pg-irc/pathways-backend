import unittest
from django.test import TestCase
from ..importer import import_organizations_file, parse_organization, parse_required_field
from .helpers import OpenReferralCsvOrganizationBuilder
from common.testhelpers.random_test_values import a_string


class OpenReferralImporterTests(TestCase):
    def test_missing_organizations_file_throws_exception(self):
        incorrect_file_path = '../foo/organizations.csv'
        with self.assertRaises(FileNotFoundError) as error:
            import_organizations_file(incorrect_file_path)


class OpenReferralParserTests(TestCase):
    def setUp(self):
        self.headers = ['id', 'name']

    def test_can_parse_id(self):
        the_id = a_string()
        organization_data = OpenReferralCsvOrganizationBuilder().with_id(the_id).build()
        organization = parse_organization(self.headers, organization_data)
        self.assertEqual(organization['id'], the_id)
    
    def test_can_parse_name(self):
        the_name = a_string()
        organization_data = OpenReferralCsvOrganizationBuilder().with_name(the_name).build()
        organization = parse_organization(self.headers, organization_data)
        self.assertEqual(organization['name'], the_name)
        

class HTMLMarkupParserTests(TestCase):
    def test_removes_doubly_escaped_bold_markup_from_required_field(self):
        the_name = '&amp;lt;b&amp;gt;abc'
        html_markup = parse_required_field('name', the_name)
        self.assertEqual(html_markup, 'abc')

    def test_removes_doubly_escaped_strong_markup_from_required_field(self):
        the_name = '&amp;lt;strong&amp;gt;abc'
        html_markup = parse_required_field('name', the_name)
        self.assertEqual(html_markup, 'abc')