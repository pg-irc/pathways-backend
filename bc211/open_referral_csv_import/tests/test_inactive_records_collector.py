from django.test import TestCase
from common.testhelpers.random_test_values import a_string
from bc211.open_referral_csv_import.inactive_records_collector import InactiveRecordsCollector
from bc211.open_referral_csv_import.organization import import_organization
from bc211.open_referral_csv_import.tests.helpers import OpenReferralCsvOrganizationBuilder

class TestInactiveRecordsCollector(TestCase):
    def setUp(self):
        self.collector = InactiveRecordsCollector()

    def test_can_add_inactive_organization_ids(self):
        the_id = a_string()
        the_description = 'DEL 15'
        inactive_organization_data = (OpenReferralCsvOrganizationBuilder()
                                    .with_id(the_id)
                                    .with_description(the_description)
                                    .build())
        import_organization(inactive_organization_data, self.collector)
        self.assertEqual(self.collector.inactive_organizations_ids[0], the_id)