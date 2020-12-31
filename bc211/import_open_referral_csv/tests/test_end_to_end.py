import string
from django.test import TestCase
from bc211.import_open_referral_csv.inactive_records_collector import InactiveRecordsCollector
from bc211.import_icarol_xml.import_counters import ImportCounters
from bc211.import_open_referral_csv.organization import import_organization
from bc211.import_open_referral_csv.service import import_service
from bc211.import_open_referral_csv.location import import_location
from bc211.import_open_referral_csv.service_at_location import import_service_at_location
from bc211.import_open_referral_csv.address import import_address, import_location_address
from bc211.import_open_referral_csv.phone import import_phone
from bc211.import_open_referral_csv.taxonomy import import_taxonomy
from bc211.import_open_referral_csv.organization import read_and_import_rows as import_organization
from bc211.import_open_referral_csv.service import read_and_import_rows as import_services
from bc211.import_open_referral_csv.taxonomy import read_and_import_rows as import_taxonomy_terms
from bc211.import_open_referral_csv.service_taxonomy import read_and_import_rows as import_service_taxonomy
from bc211.import_open_referral_csv.tests.helpers import (
    OpenReferralCsvOrganizationBuilder, OpenReferralCsvServiceBuilder,
    OpenReferralCsvLocationBuilder, OpenReferralCsvServiceAtLocationBuilder,
    OpenReferralCsvAddressBuilder, OpenReferralCsvPhoneBuilder, OpenReferralCsvTaxonomyBuilder,
    OpenReferralCsvServiceTaxonomyBuilder)
from common.testhelpers.random_test_values import (a_string, an_email_address, a_website_address,
                                                   a_latitude, a_longitude, a_phone_number, a_country_code)
from human_services.organizations.models import Organization
from human_services.organizations.tests.helpers import OrganizationBuilder
from human_services.services.tests.helpers import ServiceBuilder
from human_services.locations.tests.helpers import LocationBuilder
from human_services.services.models import Service
from human_services.locations.models import Location, ServiceAtLocation
from human_services.addresses.models import Address, AddressType
from human_services.locations.models import LocationAddress
from human_services.phone_at_location.models import PhoneNumberType, PhoneAtLocation
from taxonomies.tests.helpers import TaxonomyTermBuilder
from taxonomies.models import TaxonomyTerm
from bc211.convert_icarol_csv.tests.helpers import Bc211CsvDataBuilder
from bc211.convert_icarol_csv.parser import parse
from bc211.convert_icarol_csv.tests.test_data_sink import TestDataSink


class TaxonomyEndToEndTest(TestCase):

    def test_one_row(self):
        bc211_what_taxonomy_term = a_string(from_character_string=string.ascii_uppercase)
        data = (Bc211CsvDataBuilder().as_service().with_field('TaxonomyTerm', bc211_what_taxonomy_term).build())
        parsed_data = parse(TestDataSink(), data)
        self.assertEqual(len(parsed_data.taxonomy_terms), 1)
        self.assertEqual(parsed_data.taxonomy_terms[0]['name'], bc211_what_taxonomy_term.lower())

    def test_service_with_taxonomy_term(self):
        # all upper case taxonomy terms are by convention assigned the bc211-what taxonomy
        bc211_what_taxonomy_term = a_string().upper()
        the_organization_id = a_string()
        the_service_id = a_string()

        # create and parse the bc211 csv data for a service with a taxonomy term

        data = (Bc211CsvDataBuilder().
                as_organization().
                with_field('ResourceAgencyNum', the_organization_id).
                with_field('PublicName', a_string()).
                next_row().
                as_service().
                with_field('ResourceAgencyNum', the_service_id).
                with_field('PublicName', a_string()).
                with_field('ParentAgencyNum', the_organization_id).
                with_field('TaxonomyTerm', bc211_what_taxonomy_term).
                build())
        parsed_data = parse(TestDataSink(), data)

        self.assertEqual(len(parsed_data.organizations), 1)
        self.assertEqual(parsed_data.organizations[0]['id'], the_organization_id)

        self.assertEqual(len(parsed_data.services), 1)
        self.assertEqual(parsed_data.services[0]['organization_id'], the_organization_id)
        self.assertEqual(parsed_data.services[0]['id'], the_service_id)

        self.assertEquals(len(parsed_data.taxonomy_terms), 1)
        self.assertEquals(parsed_data.taxonomy_terms[0]['name'], bc211_what_taxonomy_term.lower())
        self.assertEquals(parsed_data.taxonomy_terms[0]['vocabulary'], 'bc211-what')
        taxonomy_term_id = parsed_data.taxonomy_terms[0]['id']

        self.assertEquals(len(parsed_data.services_taxonomy), 1)
        self.assertEquals(parsed_data.services_taxonomy[0]['service_id'], the_service_id)
        self.assertEquals(parsed_data.services_taxonomy[0]['taxonomy_id'], taxonomy_term_id)

        # import organization

        data = [[
            # id,name,alternate_name,
            r['id'], r['name'], r['alternate_name'],
            # description,email,url,
            '', '', '',
            # tax_status,tax_id,year_incorporated,legal_status
            '', '', '', '']
                for r in parsed_data.organizations]
        collector = InactiveRecordsCollector()
        counters = ImportCounters()
        import_organization(data, collector, counters)
        result = Organization.objects.all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, the_organization_id)

        # import service

        data = [[
            # id,organization_id,program_id,
            r['id'], r['organization_id'], '',
            # name,alternate_name,description,
            r['name'], r['alternate_name'], '',
            # url,email,status,
            r['url'], r['email'], '',
            # interpretation_services,application_process,wait_time,
            '', '', '',
            # fees,accreditations,licenses, taxonomy_ids,last_verified_on-x
            '', '', '', '', '']
                for r in parsed_data.services]
        import_services(data, collector, counters)
        result = Service.objects.all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, the_service_id)
        self.assertEqual(result[0].organization_id, the_organization_id)

        # import taxonomy terms

        data = [[
            # id,name,parent_id,
            r['id'], r['name'], '',
            # parent_name,vocabulary
            '', r['vocabulary']]
                for r in parsed_data.taxonomy_terms]
        import_taxonomy_terms(data, counters)
        result = TaxonomyTerm.objects.all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].taxonomy_term_id, taxonomy_term_id)
        self.assertEqual(result[0].name, bc211_what_taxonomy_term.lower())
        self.assertEqual(result[0].taxonomy_id, 'bc211-what')

        # import service taxonomy terms

        data = [[
            # id,service_id,taxonomy_id, taxonomy_detail
            r['id'], r['service_id'], r['taxonomy_id'], '']
                for r in parsed_data.services_taxonomy]
        import_service_taxonomy(data, collector)
        result = Service.objects.all()[0].taxonomy_terms.all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].taxonomy_term_id, taxonomy_term_id)
        self.assertEqual(result[0].taxonomy_id, 'bc211-what')
        self.assertEqual(result[0].name, bc211_what_taxonomy_term.lower())


# WARNING service_taxonomy TaxonomyTerm matching query does not exist.
