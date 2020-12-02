from django.test import TestCase
from common.testhelpers.random_test_values import a_string
from human_services.locations.models import Location, ServiceAtLocation
from human_services.addresses.models import Address, AddressType
from human_services.locations.models import Location, ServiceAtLocation, LocationAddress
from human_services.organizations.tests.helpers import OrganizationBuilder
from human_services.locations.tests.helpers import LocationBuilder
from human_services.addresses.tests.helpers import AddressBuilder


# Test to see how I can use Django ORM to join related locations and addresses where location.point = NULL and address.city is not NULL

class SandboxTest(TestCase):
    def setUp(self):
        organization = OrganizationBuilder().create()
        location_1_id = a_string()
        location_2_id = a_string()
        location_3_id = a_string()

        self.location_1 = LocationBuilder(organization).with_id(location_1_id).with_point(None).create()
        self.location_2 = LocationBuilder(organization).with_id(location_2_id).with_point(None).create()
        self.location_3 = LocationBuilder(organization).with_id(location_3_id).create()

        address_1_id = a_string()
        address_2_id = a_string()
        address_3_id = a_string()

        self.address_1 = AddressBuilder().with_id(address_1_id).with_city('Richmond').create()
        self.address_2 = AddressBuilder().with_id(address_2_id).with_city('Vancouver').create()
        self.address_3 = AddressBuilder().with_id(address_3_id).with_city(None).create()

        self.physical_address_type = AddressType.objects.get(pk='physical_address')

        LocationAddress(address=self.address_1, location=self.location_1, address_type=self.physical_address_type).save()
        LocationAddress(address=self.address_2, location=self.location_2, address_type=self.physical_address_type).save()
        LocationAddress(address=self.address_3, location=self.location_3, address_type=self.physical_address_type).save()
    
    def test_can_filter_locations(self):
       missing_coordinates_list = LocationAddress.objects.filter(location__point__isnull=True, address__city__isnull=False)
       self.assertEqual(missing_coordinates_list[0].address.city, 'Richmond')
       self.assertEqual(missing_coordinates_list[1].address.city, 'Vancouver')
       self.assertEqual(len(missing_coordinates_list), 2)






