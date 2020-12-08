from django.test import TestCase
from django.contrib.gis.geos import Point
from bc211.open_referral_csv_import.import_missing_coordinates import import_missing_coordinates
from common.testhelpers.random_test_values import a_string
from human_services.addresses.models import AddressType
from human_services.locations.models import Location, LocationAddress
from human_services.organizations.tests.helpers import OrganizationBuilder
from human_services.locations.tests.helpers import LocationBuilder
from human_services.addresses.tests.helpers import AddressBuilder


class ImportMissingCoordinatesTests(TestCase):
    def setUp(self):
        self.organization = OrganizationBuilder().create()
        self.physical_address_type = AddressType.objects.get(pk='physical_address')
        self.city_latlong_map = {'Vancouver': Point(-123.120738, 49.282729)}

    def test_replaces_missing_coordinates_with_city_latlong(self):
        location_id = a_string()
        location_without_point = (LocationBuilder(self.organization).
                                    with_id(location_id).
                                    with_point(None).
                                    create())
        address = AddressBuilder().with_city('Vancouver').create()
        LocationAddress(address=address,
                        location=location_without_point,
                        address_type=self.physical_address_type).save()

        import_missing_coordinates(self.city_latlong_map)
        updated_location = Location.objects.get(pk=location_id)
        self.assertEqual(updated_location.point.x, -123.120738)

    def test_does_not_replace_coordinates_when_they_are_present(self):
        location_id = a_string()
        location_with_point = (LocationBuilder(self.organization).
                                with_id(location_id).
                                with_point(Point(-123.500, 49.500)).
                                create())
        address = AddressBuilder().with_city('Vancouver').create()
        LocationAddress(address=address, 
                        location=location_with_point,
                        address_type=self.physical_address_type).save()

        import_missing_coordinates(self.city_latlong_map)
        not_updated_location = Location.objects.get(pk=location_id)
        self.assertEqual(not_updated_location.point.x, -123.500)
