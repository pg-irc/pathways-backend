import unittest
from django.test import TestCase
from ..organization import import_organizations_file, parse_organization, save_organization
from ..service import import_services_file, parse_service, save_service
from .helpers import OpenReferralCsvOrganizationBuilder, OpenReferralCsvServiceBuilder
from common.testhelpers.random_test_values import a_string, an_email_address, a_website_address
from human_services.organizations.models import Organization
from human_services.organizations.tests.helpers import OrganizationBuilder
from human_services.services.models import Service


class OpenReferralImporterTests(TestCase):
    def test_missing_organizations_file_throws_exception(self):
        incorrect_file_path = '../foo/organizations.csv'
        with self.assertRaises(FileNotFoundError) as error:
            import_organizations_file(incorrect_file_path)

    def test_missing_services_file_throws_exception(self):
        incorrect_file_path = '../foo/services.csv'
        with self.assertRaises(FileNotFoundError) as error:
            import_services_file(incorrect_file_path)


class OpenReferralOrganizationImporterTests(TestCase):
    def setUp(self):
        self.headers = ['id', 'name', 'alternate_name', 'description', 'email', 'url',
                        'tax_status', 'tax_id', 'year_incorporated', 'legal_status']

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

    def test_can_import_website(self):
        the_website = a_website_address()
        organization_data = OpenReferralCsvOrganizationBuilder().with_url(the_website).build()
        organization = parse_organization(self.headers, organization_data)
        organization.website
        save_organization(organization)
        organizations = Organization.objects.all()
        self.assertEqual(organizations[0].website, the_website)


class OpenReferralServiceImporterTests(TestCase):
    def setUp(self):
        self.headers = ['id', 'organization_id', 'program_id', 'name', 'alternate_name', 'description', 'url', 'email',
                        'status', 'interpretation_services', 'application_process', 'wait_time', 'fees', 'accreditations',
                        'licenses', 'taxonomy_ids']
        self.organization_id_passed_to_parser = a_string()
        self.organization = OrganizationBuilder().with_id(self.organization_id_passed_to_parser).build()
        self.organization.save()
    
    def test_can_import_id(self): 
        the_id = a_string()
        service_data = OpenReferralCsvServiceBuilder(self.organization).with_id(the_id).build()
        service = parse_service(self.headers, service_data)
        save_service(service)
        services = Service.objects.all()
        self.assertEqual(services[0].id, the_id)

    def test_can_import_organization_id(self):
        service_data = OpenReferralCsvServiceBuilder(self.organization).build()
        service = parse_service(self.headers, service_data)
        save_service(service)
        services = Service.objects.all()
        self.assertEqual(services[0].organization_id, self.organization_id_passed_to_parser)
    
    def test_can_import_name(self):
        the_name = a_string()
        service_data = OpenReferralCsvServiceBuilder(self.organization).with_name(the_name).build()
        service = parse_service(self.headers, service_data)
        save_service(service)
        services = Service.objects.all()
        self.assertEqual(services[0].name, the_name)
    
    def test_can_import_alternate_name(self):
        the_alternate_name = a_string()
        service_data = OpenReferralCsvServiceBuilder(self.organization).with_alternate_name(the_alternate_name).build()
        service = parse_service(self.headers, service_data)
        save_service(service)
        services = Service.objects.all()
        self.assertEqual(services[0].alternate_name, the_alternate_name)

    def test_can_import_description(self):
        the_description = a_string()
        service_data = OpenReferralCsvServiceBuilder(self.organization).with_description(the_description).build()
        service = parse_service(self.headers, service_data)
        save_service(service)
        services = Service.objects.all()
        self.assertEqual(services[0].description, the_description)
    
    def test_can_import_website(self):
        the_website = a_website_address()
        service_data = OpenReferralCsvServiceBuilder(self.organization).with_url(the_website).build()
        service = parse_service(self.headers, service_data)
        save_service(service)
        services = Service.objects.all()
        self.assertEqual(services[0].website, the_website)