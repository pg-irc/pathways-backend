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


class UpdateLocationTests(TestCase):
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
        LocationBuilder(self.organization).with_id(self.location_id).create()
        the_new_name = a_string()
        new_location_dto = (LocationBuilder(self.organization).
                            with_id(self.location_id).
                            with_name(the_new_name).
                            build_dto())

        save_locations([new_location_dto], {}, ImportCounters())

        all_locations = Location.objects.all()
        self.assertEqual(len(all_locations), 1)
        self.assertEqual(all_locations[0].id, self.location_id)
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
        location_with_new_address = (LocationBuilder(self.organization).
                                     with_id(self.location_id).
                                     with_physical_address(new_address).
                                     build_dto())
        save_locations([location_with_new_address], {}, ImportCounters())

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
        location_with_new_address = (LocationBuilder(self.organization).
                                     with_id(self.location_id).
                                     with_physical_address(new_address).
                                     build_dto())
        save_locations([location_with_new_address], {}, ImportCounters())

        location_addresses = LocationAddress.objects.filter(location_id=self.location_id)
        self.assertEqual(len(location_addresses), 1)
        self.assertEqual(location_addresses[0].address.city, new_address.city)

        addresses = Address.objects.all()
        self.assertEqual(len(addresses), 1)
        self.assertEqual(addresses[0].city, new_address.city)

    def test_saving_locations_creates_new_location_etry(self):
        save_locations([(LocationBuilder(self.organization).build_dto())], {}, ImportCounters())

        locations = Location.objects.all()
        self.assertEqual(len(locations), 1)

    def test_saving_locations_creates_new_address_entry(self):
        address = (AddressBuilder().
                   with_location_id(self.location_id).
                   with_address_type('postal_address').
                   build_dto())
        location = LocationBuilder(self.organization).with_postal_address(address).build_dto()

        save_locations([location], {}, ImportCounters())
        self.assertEqual(len(Address.objects.all()), 1)

    def test_saving_locations_creates_new_phone_number_entry(self):
        phone_at_location_dto = dtos.PhoneAtLocation(phone_number_type_id=self.phone_number_type_id,
                                                     phone_number=a_phone_number(),
                                                     location_id=self.location_id)
        location_dto = (LocationBuilder(self.organization).
                        with_id(self.location_id).
                        with_phone_numbers([phone_at_location_dto]).
                        build_dto())
        save_locations([location_dto], {}, ImportCounters())
        self.assertEqual(len(PhoneAtLocation.objects.all()), 1)

    def test_saving_locations_deletes_newly_absent_locations_from_same_organization(self):
        first_location = LocationBuilder(self.organization).create()
        second_location = LocationBuilder(self.organization).create()
        third_location = LocationBuilder(self.organization).create()

        locations = Location.objects.all()
        self.assertEqual(len(locations), 3)

        new_locations = [(LocationBuilder(self.organization).
                          with_id(first_location.id).
                          build_dto())]

        save_locations(new_locations, {}, ImportCounters())

        locations = Location.objects.all()
        self.assertEqual(len(locations), 1)
        self.assertEqual(locations[0].id, first_location.id)

    def test_saving_locations_with_newly_absent_location_removes_address_record_for_missing_location(self):
        address = (AddressBuilder().
                   with_location_id(self.location_id).
                   create())
        first_location = (LocationBuilder(self.organization).
                          with_physical_address(address).
                          create())
        self.set_physical_address(first_location, address)

        second_location = LocationBuilder(self.organization).create()

        updated_second_location = (LocationBuilder(self.organization).
                                   with_id(second_location.id).
                                   build_dto())

        self.assertEqual(len(LocationAddress.objects.all()), 1)

        save_locations([updated_second_location], {}, ImportCounters())

        self.assertEqual(len(LocationAddress.objects.all()), 0)

    def test_saving_locations_with_newly_absent_location_removes_phone_nubmer_record(self):
        location = (LocationBuilder(self.organization). create())
        PhoneAtLocation.objects.create(phone_number_type=self.phone_number_type,
                                       phone_number=a_phone_number(),
                                       location=location)
        self.assertEqual(len(PhoneAtLocation.objects.all()), 1)

        second_location = LocationBuilder(self.organization).build_dto()

        save_locations([second_location], {}, ImportCounters())

        self.assertEqual(len(PhoneAtLocation.objects.all()), 0)

    def test_saving_locations_does_not_cause_deletion_of_locations_for_other_organization(self):
        first_organization = OrganizationBuilder().create()
        first_location = LocationBuilder(first_organization).create()

        second_organization = OrganizationBuilder().create()
        second_location = LocationBuilder(second_organization).create()

        save_locations([(LocationBuilder(second_organization).
                         with_id(second_location.id).
                         build_dto())], {}, ImportCounters())

        location_ids = [location.id for location in Location.objects.all()]
        self.assertEqual(len(location_ids), 2)
        self.assertIn(first_location.id, location_ids)
        self.assertIn(second_location.id, location_ids)
