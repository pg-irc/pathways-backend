from django.test import TestCase
from bc211.importer import save_locations
from bc211.import_counters import ImportCounters
from human_services.organizations.tests.helpers import OrganizationBuilder
from human_services.locations.models import Location
from human_services.locations.tests.helpers import LocationBuilder
from common.testhelpers.random_test_values import a_string


class LocationUpdateTests(TestCase):
    def test_update_existing_location(self):
        organization = OrganizationBuilder().create()
        the_id = a_string()
        LocationBuilder(organization).with_id(the_id).create()
        the_new_name = a_string()
        new_location_dto = (LocationBuilder(organization).
                            with_id(the_id).
                            with_name(the_new_name).
                            build_dto())

        save_locations([new_location_dto], {}, ImportCounters())

        all_locations = Location.objects.all()
        self.assertEqual(len(all_locations), 1)
        self.assertEqual(all_locations[0].id, the_id)
        self.assertEqual(all_locations[0].name, new_location_dto.name)


class LocationDeleteTest(TestCase):
    pass
