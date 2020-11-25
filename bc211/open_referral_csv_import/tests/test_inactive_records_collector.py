from django.test import TestCase
from common.testhelpers.random_test_values import a_string
from bc211.open_referral_csv_import.inactive_records_collector import InactiveRecordsCollector
from bc211.open_referral_csv_import.organization import import_organization
from bc211.open_referral_csv_import.service import import_service, has_inactive_organization_id
from bc211.open_referral_csv_import.tests import helpers
from human_services.organizations.tests.helpers import OrganizationBuilder


class TestInactiveRecordsCollector(TestCase):
    def setUp(self):
        self.collector = InactiveRecordsCollector()
        self.the_description = 'DEL16'
        self.organization = OrganizationBuilder().create()

    def test_can_add_inactive_organization_ids(self):
        the_id = a_string()
        inactive_organization_data = (helpers.OpenReferralCsvOrganizationBuilder()
                                    .with_id(the_id)
                                    .with_description(self.the_description)
                                    .build())
        import_organization(inactive_organization_data, self.collector)
        self.assertEqual(self.collector.inactive_organizations_ids[0], the_id)
    
    def test_can_add_inactive_service_ids(self):
        the_id = a_string()
        inactive_services_data = (helpers.OpenReferralCsvServiceBuilder(self.organization)
                                .with_id(the_id)
                                .with_description(self.the_description)
                                .build())
        import_service(inactive_services_data, self.collector)
        self.assertEqual(self.collector.inactive_services_ids[0], the_id)
        
    def test_returns_true_when_organization_id_is_in_inactive_organizations_list(self):
        organization_id = a_string()
        self.collector.add_inactive_organization_id(a_string())
        self.collector.add_inactive_organization_id(organization_id)
        self.collector.add_inactive_organization_id(a_string())
        self.assertTrue(has_inactive_organization_id(organization_id, self.collector))
        
