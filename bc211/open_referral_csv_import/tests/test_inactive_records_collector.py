from django.test import TestCase
from common.testhelpers.random_test_values import a_string
from bc211.open_referral_csv_import.inactive_records_collector import InactiveRecordsCollector
from bc211.open_referral_csv_import.organization import organization_has_inactive_data
from bc211.open_referral_csv_import.service import service_has_inactive_data
from bc211.open_referral_csv_import.location import location_has_inactive_data
from bc211.open_referral_csv_import.inactive_foreign_key import (has_inactive_organization_id,
                                                            has_inactive_service_id,
                                                            has_inactive_location_id)
from bc211.open_referral_csv_import.tests import helpers
from human_services.organizations.tests.helpers import OrganizationBuilder


class TestInactiveRecordsCollector(TestCase):
    def setUp(self):
        self.collector = InactiveRecordsCollector()
        self.the_description = 'DEL16'
        self.organization = OrganizationBuilder().create()

    def test_can_add_inactive_organization_id(self):
        the_id = a_string()
        inactive_organization_data = (helpers.OpenReferralCsvOrganizationBuilder()
                                    .with_id(the_id)
                                    .with_description(self.the_description)
                                    .build())
        organization_has_inactive_data(inactive_organization_data, self.collector)
        self.assertEqual(self.collector.inactive_organizations_ids[0], the_id)
    
    def test_can_add_inactive_service_id(self):
        the_id = a_string()
        inactive_service_data = (helpers.OpenReferralCsvServiceBuilder(self.organization)
                                .with_id(the_id)
                                .with_description(self.the_description)
                                .build())
        service_has_inactive_data(inactive_service_data, self.collector)
        self.assertEqual(self.collector.inactive_services_ids[0], the_id)

    def test_can_add_inactive_location_id(self):
        the_id = a_string()
        inactive_location_data = (helpers.OpenReferralCsvLocationBuilder(self.organization)
                                .with_id(the_id)
                                .with_description(self.the_description)
                                .build())
        location_has_inactive_data(inactive_location_data, self.collector)
        self.assertEqual(self.collector.inactive_locations_ids[0], the_id)
        
    def test_returns_true_when_organization_id_is_in_inactive_organizations_list(self):
        organization_id = a_string()
        self.collector.add_inactive_organization_id(a_string())
        self.collector.add_inactive_organization_id(organization_id)
        self.collector.add_inactive_organization_id(a_string())
        self.assertTrue(has_inactive_organization_id(organization_id, self.collector))
        
    def test_returns_true_when_service_id_is_in_inactive_services_list(self):
        service_id = a_string()
        self.collector.add_inactive_service_id(a_string())
        self.collector.add_inactive_service_id(a_string())
        self.collector.add_inactive_service_id(service_id)
        self.assertTrue(has_inactive_service_id(service_id, self.collector))
    
    def test_returns_true_when_location_id_is_in_inactive_locations_list(self):
        location_id = a_string()
        self.collector.add_inactive_location_id(a_string())
        self.collector.add_inactive_location_id(a_string())
        self.collector.add_inactive_location_id(location_id)
        self.assertTrue(has_inactive_location_id(location_id, self.collector))
