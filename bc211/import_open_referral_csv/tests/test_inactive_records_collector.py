from django.test import TestCase
from common.testhelpers.random_test_values import a_string, an_integer
from bc211.import_open_referral_csv.inactive_records_collector import InactiveRecordsCollector
from human_services.organizations.tests.helpers import OrganizationBuilder

#  TODO are there even inactive locations? verify
class TestInactiveRecordsCollector(TestCase):
    def setUp(self):
        self.collector = InactiveRecordsCollector()
        self.the_description = 'DEL' + str(an_integer(min=10, max=99))
        self.organization_id = a_string()
        self.organization = OrganizationBuilder().with_id(self.organization_id).create()

    def test_can_add_inactive_organization_id(self):
        the_id = a_string()
        self.collector.organization_has_inactive_data(the_id, self.the_description)
        self.assertEqual(self.collector.inactive_organizations_ids[0], the_id)

    def test_can_add_inactive_service_id(self):
        the_id = a_string()
        self.collector.service_has_inactive_data(self.organization_id, the_id, self.the_description)
        self.assertEqual(self.collector.inactive_services_ids[0], the_id)

    def test_can_add_inactive_location_id(self):
        the_id = a_string()
        self.collector.location_has_inactive_data(
            self.organization_id,
            the_id,
            self.the_description)
        self.assertEqual(self.collector.inactive_locations_ids[0], the_id)

    def test_returns_true_when_organization_id_is_in_inactive_organizations_list(self):
        organization_id = a_string()
        self.collector.add_inactive_organization_id(a_string())
        self.collector.add_inactive_organization_id(organization_id)
        self.collector.add_inactive_organization_id(a_string())
        self.assertTrue(self.collector.has_inactive_organization_id(organization_id))

    def test_returns_true_when_service_id_is_in_inactive_services_list(self):
        service_id = a_string()
        self.collector.add_inactive_service_id(a_string())
        self.collector.add_inactive_service_id(a_string())
        self.collector.add_inactive_service_id(service_id)
        self.assertTrue(self.collector.has_inactive_service_id(service_id))

    def test_returns_true_when_location_id_is_in_inactive_locations_list(self):
        location_id = a_string()
        self.collector.add_inactive_location_id(a_string())
        self.collector.add_inactive_location_id(a_string())
        self.collector.add_inactive_location_id(location_id)
        self.assertTrue(self.collector.has_inactive_location_id(location_id))
