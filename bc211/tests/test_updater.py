from django.test import TestCase
from bc211 import dtos
from bc211.importer import save_locations
from bc211.import_counters import ImportCounters
from human_services.addresses.models import Address, AddressType
from human_services.addresses.tests.helpers import AddressBuilder
from human_services.organizations.tests.helpers import OrganizationBuilder
from human_services.locations.models import Location, LocationAddress
from human_services.locations.tests.helpers import LocationBuilder
from human_services.phone_at_location.models import PhoneAtLocation, PhoneNumberType
from common.testhelpers.random_test_values import a_phone_number, a_string


class LocationUpdateTests(TestCase):
    def setUp(self):
        self.location_id = a_string()
        self.organization = OrganizationBuilder().create()
        self.physical_address_type = AddressType.objects.get(pk='physical_address')
        self.postal_address_type = AddressType.objects.get(pk='postal_address')
        self.phone_number_type_id = a_string()
        self.phone_number_type = PhoneNumberType.objects.create(id=self.phone_number_type_id)

    def set_physical_address(self, location, address):
        LocationAddress(address=address, location=location,
                        address_type=self.physical_address_type).save()

    def set_postal_address(self, location, address):
        LocationAddress(address=address, location=location,
                        address_type=self.postal_address_type).save()

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

    def test_update_phone_number_on_existing_location(self):
        location = (LocationBuilder(self.organization).
                    with_id(self.location_id).
                    create())
        PhoneAtLocation.objects.create(phone_number_type=self.phone_number_type,
                                       phone_number=a_phone_number(),
                                       location=location)
        new_phone_number = a_phone_number()
        new_phone_at_location_dto = dtos.PhoneAtLocation(phone_number_type_id=self.phone_number_type_id,
                                                         phone_number=new_phone_number,
                                                         location_id=self.location_id)

        location_with_new_number = (LocationBuilder(self.organization).
                                    with_id(self.location_id).
                                    with_phone_numbers([new_phone_at_location_dto]).
                                    build_dto())

        save_locations([location_with_new_number], {}, ImportCounters())

        phone_numbers = PhoneAtLocation.objects.all()
        self.assertEqual(len(phone_numbers), 1)
        self.assertEqual(phone_numbers[0].phone_number, new_phone_number)

    def test_changing_physical_address_on_location_replaces_address_record(self):
        old_address = (AddressBuilder().
                       with_location_id(self.location_id).
                       create())
        location = (LocationBuilder(self.organization).
                    with_id(self.location_id).
                    with_physical_address(old_address).
                    create())

        self.set_physical_address(location, old_address)

        new_address = (AddressBuilder().
                       with_location_id(self.location_id).
                       with_address_type('physical_address').
                       build_dto())
        location = (LocationBuilder(self.organization).
                    with_id(self.location_id).
                    with_physical_address(new_address).
                    build_dto())
        save_locations([location], {}, ImportCounters())

        location_addresses = LocationAddress.objects.filter(location_id=self.location_id)
        self.assertEqual(len(location_addresses), 1)
        self.assertEqual(location_addresses[0].address.city, new_address.city)

        addresses = Address.objects.all()
        self.assertEqual(len(addresses), 1)
        self.assertEqual(addresses[0].city, new_address.city)

    def test_changing_postal_address_on_location_replaces_address_record(self):
        old_address = (AddressBuilder().
                       with_location_id(self.location_id).
                       create())
        location = (LocationBuilder(self.organization).
                    with_id(self.location_id).
                    with_physical_address(old_address).
                    create())

        self.set_postal_address(location, old_address)

        new_address = (AddressBuilder().
                       with_location_id(self.location_id).
                       with_address_type('postal_address').
                       build_dto())
        location = (LocationBuilder(self.organization).
                    with_id(self.location_id).
                    with_physical_address(new_address).
                    build_dto())
        save_locations([location], {}, ImportCounters())

        location_addresses = LocationAddress.objects.filter(location_id=self.location_id)
        self.assertEqual(len(location_addresses), 1)
        self.assertEqual(location_addresses[0].address.city, new_address.city)

        addresses = Address.objects.all()
        self.assertEqual(len(addresses), 1)
        self.assertEqual(addresses[0].city, new_address.city)
