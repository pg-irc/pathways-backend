from django.test import TestCase
from bc211 import dtos
from bc211.importer import save_locations
from bc211.import_counters import ImportCounters
from human_services.addresses.models import Address
from human_services.addresses.tests.helpers import AddressBuilder
from human_services.organizations.tests.helpers import OrganizationBuilder
from human_services.locations.models import Location, LocationAddress
from human_services.locations.tests.helpers import LocationBuilder
from human_services.phone_at_location.models import PhoneAtLocation
from common.testhelpers.random_test_values import a_phone_number, a_string


class LocationUpdateTests(TestCase):
    def setUp(self):
        self.location_id = a_string()
        self.organization = OrganizationBuilder().create()

    def test_update_existing_location(self):
        the_id = a_string()
        LocationBuilder(self.organization).with_id(the_id).create()
        the_new_name = a_string()
        new_location_dto = (LocationBuilder(self.organization).
                            with_id(the_id).
                            with_name(the_new_name).
                            build_dto())

        save_locations([new_location_dto], {}, ImportCounters())

        all_locations = Location.objects.all()
        self.assertEqual(len(all_locations), 1)
        self.assertEqual(all_locations[0].id, the_id)
        self.assertEqual(all_locations[0].name, new_location_dto.name)

    def test_changing_phone_number_on_location_replaces_phone_number_record(self):
        phone_number_type_id = a_string()
        new_phone_number = a_phone_number()

        phone_at_location = dtos.PhoneAtLocation(phone_number_type_id=phone_number_type_id,
                                                 phone_number=a_phone_number(),
                                                 location_id=self.location_id)
        location_builder = (LocationBuilder(self.organization).
                            with_id(self.location_id).
                            with_phone_numbers([phone_at_location]))

        save_locations([location_builder.build_dto()], {}, ImportCounters())

        new_phone_at_location = dtos.PhoneAtLocation(phone_number_type_id=phone_number_type_id,
                                                     phone_number=new_phone_number,
                                                     location_id=self.location_id)
        save_locations(
            [(location_builder.
              with_phone_numbers([new_phone_at_location]).
              build_dto())
             ], {}, ImportCounters())

        phone_numbers = PhoneAtLocation.objects.all()
        self.assertEqual(len(phone_numbers), 1)
        self.assertEqual(phone_numbers[0].phone_number, new_phone_number)

    def test_changing_physical_address_on_location_replaces_address_record(self):
        address = (AddressBuilder().
                   with_location_id(self.location_id).
                   with_address_type('physical_address'))
        location_builder = (LocationBuilder(self.organization).
                            with_id(self.location_id).
                            with_physical_address(address.build_dto()))

        save_locations([location_builder.build_dto()], {}, ImportCounters())

        new_address = (AddressBuilder().
                       with_location_id(self.location_id).
                       with_address_type('physical_address').
                       build_dto())
        save_locations([(location_builder.
                         with_physical_address(new_address).
                         build_dto())], {}, ImportCounters())

        location_addresses = LocationAddress.objects.filter(location_id=self.location_id)
        self.assertEqual(len(location_addresses), 1)
        self.assertEqual(location_addresses[0].address.city, new_address.city)

        addresses = Address.objects.all()
        self.assertEqual(len(addresses), 1)
        self.assertEqual(addresses[0].city, new_address.city)
