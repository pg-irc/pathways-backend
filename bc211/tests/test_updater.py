from django.test import TestCase
from bc211 import dtos
from bc211.importer import save_locations, save_organization_with_locations_and_services
from bc211.import_counters import ImportCounters
from human_services.addresses.models import Address, AddressType
from human_services.addresses.tests.helpers import AddressBuilder
from human_services.organizations.tests.helpers import OrganizationBuilder
from human_services.locations.models import Location, LocationAddress, ServiceAtLocation
from human_services.locations.tests.helpers import LocationBuilder
from human_services.organizations.models import Organization
from human_services.phone_at_location.models import PhoneAtLocation, PhoneNumberType
from human_services.services.models import Service
from human_services.services.tests.helpers import ServiceBuilder
from common.testhelpers.random_test_values import a_phone_number, a_string, a_float


class UpdateOrganizationTests(TestCase):

    def test_can_update_an_organization(self):
        old_organization = OrganizationBuilder().create()
        new_organization = OrganizationBuilder().with_id(old_organization.id).build_dto()

        save_organization_with_locations_and_services(new_organization, {}, ImportCounters())

        organizations = Organization.objects.all()
        self.assertEqual(organizations[0].name, new_organization.name)

    def test_can_create_a_new_organization(self):
        organization = OrganizationBuilder().build_dto()
        save_organization_with_locations_and_services(organization, {}, ImportCounters())

        organizations = Organization.objects.all()
        self.assertEqual(len(organizations), 1)
        self.assertEqual(organizations[0].id, organization.id)

    def test_can_delete_newly_absent_organization(self):
        pass

    def test_can_create_new_location_record(self):
        organization = OrganizationBuilder().create()

        location = LocationBuilder(organization).build_dto()
        organization_with_location = (OrganizationBuilder().
                                      with_id(organization.id).
                                      with_locations([location]).
                                      build_dto())

        save_organization_with_locations_and_services(organization_with_location, {}, ImportCounters())

        locations = Location.objects.all()
        self.assertEqual(len(locations), 1)
        self.assertEqual(locations[0].id, location.id)

    def test_that_newly_absent_location_is_removed(self):
        organization = OrganizationBuilder().create()
        LocationBuilder(organization).create()
        new_organization_without_location_dto = OrganizationBuilder().with_id(organization.id).build_dto()

        save_organization_with_locations_and_services(new_organization_without_location_dto, {}, ImportCounters())

        self.assertEqual(len(Location.objects.all()), 0)

    def test_can_create_new_service_record(self):
        organization = OrganizationBuilder().create()
        location = LocationBuilder(organization).create()

        service_dto = (ServiceBuilder(organization).
                       with_location(location).
                       build_dto())
        location_dto = (LocationBuilder(organization).
                        with_id(location.id).
                        with_services([service_dto]).
                        build_dto())
        new_organization_dto = (OrganizationBuilder().
                                with_id(organization.id).
                                with_locations([location_dto]).
                                build_dto())
        save_organization_with_locations_and_services(new_organization_dto, {}, ImportCounters())

        services = Service.objects.all()
        self.assertEqual(len(services), 1)
        self.assertEqual(services[0].id, service_dto.id)

        sal = ServiceAtLocation.objects.all()
        self.assertEqual(len(sal), 1)
        self.assertEqual(sal[0].location.id, location_dto.id)
        self.assertEqual(sal[0].service.id, service_dto.id)

    def test_that_a_new_service_under_a_location_is_created(self):
        pass

    def test_that_a_removed_service_under_a_location_causes_service_to_be_deleted(self):
        organization = OrganizationBuilder().create()
        location = (LocationBuilder(organization).
                    with_long_lat(a_float(), a_float()).
                    create())
        ServiceBuilder(organization).with_location(location).create()

        self.assertEqual(len(Service.objects.all()), 1)
        # TODO Move this to the more specific test below
        self.assertEqual(len(ServiceAtLocation.objects.all()), 1)

        new_location = (LocationBuilder(organization).
                        with_id(location.id).
                        with_long_lat(a_float(), a_float()).
                        build_dto())
        new_organization = (OrganizationBuilder().
                            with_id(organization.id).
                            with_locations([new_location]).
                            build_dto())

        save_organization_with_locations_and_services(new_organization, {}, ImportCounters())

        self.assertEqual(len(Service.objects.all()), 0)
        # TODO Move this to the more specific test below
        self.assertEqual(len(ServiceAtLocation.objects.all()), 0)

    def test_that_service_under_different_location_is_not_deleted(self):
        pass

    def test_that_service_in_input_is_not_deleted(self):
        organization = OrganizationBuilder().create()
        location = LocationBuilder(organization).with_long_lat(a_float(), a_float()).create()
        service_id = a_string()
        first_service_builder = ServiceBuilder(organization).with_id(service_id).with_location(location)
        second_service_builder = ServiceBuilder(organization).with_location(location)

        first_service_builder.create()
        second_service_builder.create()

        new_location = (LocationBuilder(organization).
                        with_id(location.id).
                        with_services([first_service_builder.build_dto()]).
                        build_dto())
        new_organization = (OrganizationBuilder().
                            with_id(organization.id).
                            with_locations([new_location]).
                            build_dto())
        save_organization_with_locations_and_services(new_organization, {}, ImportCounters())

        self.assertEqual(len(Service.objects.all()), 1)
        self.assertEqual(Service.objects.all()[0].id, service_id)

    # TODO test records newly marked as inactive

    def test_that_service_under_different_organization_is_not_deleted(self):
        pass

    def test_that_a_removed_service_under_a_location_causes_serviceatlocation_to_be_deleted(self):
        pass

    def test_that_a_removed_service_under_a_location_causes_taxonomy_term_to_be_deleted(self):
        pass

    def test_that_a_removed_service_under_a_location_causes_taskservicesimilarity_to_be_deleted(self):
        pass

    def test_that_changes_to_a_service_under_a_location_are_saved(self):
        pass

    def test_that_changes_to_service_taxonomy_terms_are_saved(self):
        pass

    # def test_can_remove_existing_service_record(self):
    #     # for a given location, find all related services through the ServiceAtLocation
    #     # relation, compare list of these ids with the incoming ones, remove newly absent
    #     # services, with their related ServiceAtLocation and Taxonomy bridging rows
    #     organization = OrganizationBuilder().create()
    #     location = LocationBuilder(organization).create()
    #     ServiceBuilder(organization).with_location(location).create()

    #     self.assertEqual(len(Service.objects.all()), 1)
    #     self.assertEqual(len(ServiceAtLocation.objects.all()), 1)

    #     location_dto_without_service = (LocationBuilder(organization).
    #                                     with_id(location.id).
    #                                     build_dto())
    #     new_organization_dto = (OrganizationBuilder().with_id(organization.id).
    #                             with_locations([location_dto_without_service]).
    #                             build_dto())
    #     save_organization_with_locations_and_services(new_organization_dto, {}, ImportCounters())

    #     self.assertEqual(len(Service.objects.all()), 0)
    #     self.assertEqual(len(ServiceAtLocation.objects.all()), 0)

    def test_does_not_remove_service_record_for_unrelated_organization(self):
        pass


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

        save_locations([new_location_dto], self.organization.id, {}, ImportCounters())

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

        save_locations([location_with_new_number], self.organization.id, {}, ImportCounters())

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
        save_locations([location_with_new_address], self.organization.id, {}, ImportCounters())

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
        save_locations([location_with_new_address], self.organization.id, {}, ImportCounters())

        location_addresses = LocationAddress.objects.filter(location_id=self.location_id)
        self.assertEqual(len(location_addresses), 1)
        self.assertEqual(location_addresses[0].address.city, new_address.city)

        addresses = Address.objects.all()
        self.assertEqual(len(addresses), 1)
        self.assertEqual(addresses[0].city, new_address.city)

    def test_saving_locations_creates_new_location_entry(self):
        save_locations([(LocationBuilder(self.organization).build_dto())], self.organization.id, {}, ImportCounters())

        locations = Location.objects.all()
        self.assertEqual(len(locations), 1)

    def test_saving_locations_creates_new_address_entry(self):
        address = (AddressBuilder().
                   with_location_id(self.location_id).
                   with_address_type('postal_address').
                   build_dto())
        location = LocationBuilder(self.organization).with_postal_address(address).build_dto()

        save_locations([location], self.organization.id, {}, ImportCounters())
        self.assertEqual(len(Address.objects.all()), 1)

    def test_saving_locations_creates_new_phone_number_entry(self):
        phone_at_location_dto = dtos.PhoneAtLocation(phone_number_type_id=self.phone_number_type_id,
                                                     phone_number=a_phone_number(),
                                                     location_id=self.location_id)
        location_dto = (LocationBuilder(self.organization).
                        with_id(self.location_id).
                        with_phone_numbers([phone_at_location_dto]).
                        build_dto())
        save_locations([location_dto], self.organization.id, {}, ImportCounters())
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

        save_locations(new_locations, self.organization.id, {}, ImportCounters())

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

        save_locations([updated_second_location], self.organization.id, {}, ImportCounters())

        self.assertEqual(len(LocationAddress.objects.all()), 0)

    def test_saving_locations_with_newly_absent_location_removes_phone_nubmer_record(self):
        location = (LocationBuilder(self.organization). create())
        PhoneAtLocation.objects.create(phone_number_type=self.phone_number_type,
                                       phone_number=a_phone_number(),
                                       location=location)
        self.assertEqual(len(PhoneAtLocation.objects.all()), 1)

        second_location = LocationBuilder(self.organization).build_dto()

        save_locations([second_location], self.organization.id, {}, ImportCounters())

        self.assertEqual(len(PhoneAtLocation.objects.all()), 0)

    def test_saving_locations_does_not_cause_deletion_of_locations_for_other_organization(self):
        first_organization = OrganizationBuilder().create()
        first_location = LocationBuilder(first_organization).create()

        second_organization = OrganizationBuilder().create()
        second_location = LocationBuilder(second_organization).create()

        save_locations([(LocationBuilder(second_organization).
                         with_id(second_location.id).
                         build_dto())], second_organization.id, {}, ImportCounters())

        location_ids = [location.id for location in Location.objects.all()]
        self.assertEqual(len(location_ids), 2)
        self.assertIn(first_location.id, location_ids)
        self.assertIn(second_location.id, location_ids)


class UpdateServiceTests(TestCase):
    pass
