import logging
from bc211.importer import save_records_to_database
from bc211.parser import read_records_from_file
from django.test import TestCase
from human_services.locations.models import Location
from human_services.organizations.models import Organization
from taxonomies.models import TaxonomyTerm
from services.models import Service
from human_services.addresses.models import Address, AddressType

logging.disable(logging.ERROR)

ONE_AGENCY_FIXTURE = 'bc211/data/BC211_data_one_agency.xml'
MULTI_AGENCY_FIXTURE = 'bc211/data/BC211_data_excerpt.xml'

class LocationImportTests(TestCase):
    def setUp(self):
        file = open(ONE_AGENCY_FIXTURE, 'r')
        records = read_records_from_file(file)
        save_records_to_database(records)
        all_records_from_database = Location.objects.all()
        self.location = all_records_from_database[0]

    def test_can_import_name(self):
        self.assertEqual(self.location.name, 'Langley Child Development Centre')

    def test_can_import_description(self):
        self.assertEqual(self.location.description[:30], 'Provides inclusive, family-cen')

    def test_can_import_latitude(self):
        self.assertAlmostEqual(self.location.latitude, 49.087284)

    def test_can_import_longitude(self):
        self.assertAlmostEqual(self.location.longitude, -122.607918)


class OrganizationImportTests(TestCase):
    def setUp(self):
        save_records_to_database(read_records_from_file(open(ONE_AGENCY_FIXTURE, 'r')))
        organizations = Organization.objects.all()
        self.organization = organizations[0]

    def test_can_import_id(self):
        self.assertEqual(self.organization.id, '9487364')

    def test_can_import_name(self):
        self.assertEqual(self.organization.name, 'Langley Child Development Centre')

    def test_can_import_description(self):
        self.assertEqual(self.organization.description[:30], 'Provides inclusive, family-cen')

    def test_can_import_website(self):
        self.assertEqual(self.organization.website, 'http://www.langleycdc.com')

    def test_can_import_email(self):
        self.assertEqual(self.organization.email, 'info@langleycdc.com')

class ServiceImportTests(TestCase):
    def setUp(self):
        file = open(MULTI_AGENCY_FIXTURE, 'r')
        save_records_to_database(read_records_from_file(file))
        self.all_taxonomy_terms = TaxonomyTerm.objects.all()
        self.all_services = Service.objects.all()

    def test_service_has_correct_taxonomy_terms(self):
        last_post_fund_service_id = 9487370
        expected_last_post_fund_service_taxonony_terms = [
            self.all_taxonomy_terms.get(taxonomy_id='bc211-what', name='financial-assistance'),
            self.all_taxonomy_terms.get(taxonomy_id='bc211-why', name='funerals'),
            self.all_taxonomy_terms.get(taxonomy_id='bc211-who', name='veterans'),
        ]

        last_post_fund_service = self.all_services.get(id=last_post_fund_service_id)
        last_post_fund_service_taxonomy_terms = last_post_fund_service.taxonomy_terms.all()

        self.assertCountEqual(last_post_fund_service_taxonomy_terms, expected_last_post_fund_service_taxonony_terms)


class AddressImportTests(TestCase):
    def setUp(self):
        file = open(ONE_AGENCY_FIXTURE, 'r')
        records = read_records_from_file(file)
        save_records_to_database(records)
        self.addresses = Address.objects.all()

    def test_can_import_address(self):
        self.assertIsInstance(self.addresses.first(), Address)

    def test_does_not_import_duplicates(self):
        self.assertEqual(len(self.addresses), 1)

class AddressTypeTests(TestCase):
    def test_imports_correct_address_types(self):
        expected_address_types = [
            AddressType(id='physical_address'),
            AddressType(id='postal_address')
        ]
        self.assertCountEqual(AddressType.objects.all(), expected_address_types)


class FullDataImportTests(TestCase):
    def setUp(self):
        file = open(MULTI_AGENCY_FIXTURE, 'r')
        self.return_value = save_records_to_database(read_records_from_file(file))
        self.all_locations = Location.objects.all()
        self.all_organizations = Organization.objects.all()
        self.all_taxonomy_terms = TaxonomyTerm.objects.all()

    def test_can_import_multiple_organizations(self):
        self.assertEqual(len(self.all_organizations), 16)

    def test_can_import_multiple_locations(self):
        self.assertEqual(len(self.all_locations), 40)

    def test_can_import_multiple_taxonomy_terms(self):
        self.assertEqual(len(self.all_taxonomy_terms), 134)

    def test_returns_number_of_organizations_imported(self):
        self.assertEqual(self.return_value.organization_count, 16)

    def test_returns_number_of_locations_imported(self):
        self.assertEqual(self.return_value.location_count, 40)

    def test_returns_number_of_taxonomy_terms_imported(self):
        self.assertEqual(self.return_value.taxonomy_term_count, 134)

    def test_returns_number_of_addresses_imported(self):
        self.assertEqual(self.return_value.address_count, 32)
