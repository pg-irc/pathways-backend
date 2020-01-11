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
from human_services.services_at_location.tests.helpers import set_service_similarity_score
from common.testhelpers.random_test_values import a_phone_number, a_string, a_float
from search.models import Task, TaskServiceSimilarityScore
from taxonomies.models import TaxonomyTerm
from taxonomies.tests.helpers import TaxonomyTermBuilder

# def test_that_new_C_under_P_creates_record(self):
# def test_that_newly_absent_C_under_P_is_removed(self):
# def test_that_C_under_newly_absent_P_is_removed(self):
# def test_that_newly_inactive_C_under_P_is_removed(self):
# def test_that_changed_C_under_P_is_updated(self):
# def test_that_C_under_different_P_is_not_deleted(self):
# def test_saving_C_does_not_cause_deletion_of_Cs_for_other_Ps(self):


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

    def test_that_changed_organization_is_updated(self):
        organization = OrganizationBuilder().create()
        new_organization = OrganizationBuilder().with_id(organization.id).build_dto()

        save_organization_with_locations_and_services(new_organization, {}, ImportCounters())

        organizations = Organization.objects.all()
        self.assertEqual(len(organizations), 1)
        self.assertEqual(organizations[0].name, new_organization.name)

    def test_can_delete_newly_absent_organization(self):
        pass

    def test_can_delete_newly_inactive_organization(self):
        pass


class LocationsUnderOrganizationTests(TestCase):

    def test_that_new_location_under_organization_creates_record(self):
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

    def test_that_newly_absent_locations_under_organization_is_removed(self):
        organization = OrganizationBuilder().create()
        first_location = LocationBuilder(organization).create()
        second_location = LocationBuilder(organization).create()

        locations = Location.objects.all()
        self.assertEqual(len(locations), 2)

        new_locations = [(LocationBuilder(organization).
                          with_id(first_location.id).
                          build_dto())]

        save_locations(new_locations, organization.id, {}, ImportCounters())

        locations = Location.objects.all()
        self.assertEqual(len(locations), 1)
        self.assertEqual(locations[0].id, first_location.id)

    def test_that_newly_inactive_location_under_organization_is_removed(self):
        organization = OrganizationBuilder().create()
        location = LocationBuilder(organization).create()
        inactive_location = LocationBuilder(organization).with_id(location.id).with_description('DEL').build_dto()
        new_organization = (OrganizationBuilder().
                            with_id(organization.id).
                            with_locations([inactive_location]).
                            build_dto())

        save_organization_with_locations_and_services(new_organization, {}, ImportCounters())

        self.assertEqual(len(Location.objects.all()), 0)

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

    def test_that_changed_location_under_organization_is_updated(self):
        organization = OrganizationBuilder().create()
        location_id = a_string()
        LocationBuilder(organization).with_id(location_id).create()
        new_location_dto = (LocationBuilder(organization).
                            with_id(location_id).
                            build_dto())

        save_locations([new_location_dto], organization.id, {}, ImportCounters())

        all_locations = Location.objects.all()
        self.assertEqual(len(all_locations), 1)
        self.assertEqual(all_locations[0].id, location_id)
        self.assertEqual(all_locations[0].name, new_location_dto.name)


class ServicesUnderLocationTests(TestCase):

    def test_that_new_service_under_location_creates_record(self):
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

    def test_that_newly_absent_service_under_location_is_removed(self):
        organization = OrganizationBuilder().create()
        location = LocationBuilder(organization).create()
        ServiceBuilder(organization).with_location(location).create()

        location_without_service = (LocationBuilder(organization).
                                    with_id(location.id).
                                    build_dto())
        new_organization = (OrganizationBuilder().
                            with_id(organization.id).
                            with_locations([location_without_service]).
                            build_dto())

        save_organization_with_locations_and_services(new_organization, {}, ImportCounters())

        self.assertEqual(len(Service.objects.all()), 0)
        self.assertEqual(len(ServiceAtLocation.objects.all()), 0)

    def test_that_newly_inactive_service_under_location_is_removed(self):
        organization = OrganizationBuilder().create()
        location = (LocationBuilder(organization).create())
        service = ServiceBuilder(organization).with_location(location).create()

        inactive_service = (ServiceBuilder(organization).
                            with_id(service.id).
                            with_description('DEL').
                            with_location(location).
                            build_dto())
        location_with_inactive_service = (LocationBuilder(organization).
                                          with_id(location.id).
                                          with_services([inactive_service]).
                                          build_dto())
        new_organization = (OrganizationBuilder().
                            with_id(organization.id).
                            with_locations([location_with_inactive_service]).
                            build_dto())

        save_organization_with_locations_and_services(new_organization, (), ImportCounters())

        self.assertEqual(len(Service.objects.all()), 0)
        self.assertEqual(len(ServiceAtLocation.objects.all()), 0)

    def test_that_changed_service_under_location_is_updated(self):
        organization = OrganizationBuilder().create()
        location = LocationBuilder(organization).create()
        service = ServiceBuilder(organization).with_location(location).create()

        new_service = ServiceBuilder(organization).with_id(service.id).with_location(location).build_dto()
        new_location = LocationBuilder(organization).with_id(location.id).with_services([new_service]).build_dto()
        new_organization = OrganizationBuilder().with_id(organization.id).with_locations([new_location]).build_dto()

        save_organization_with_locations_and_services(new_organization, {}, ImportCounters())

        self.assertEqual(len(Service.objects.all()), 1)
        self.assertEqual(Service.objects.all()[0].name, new_service.name)

    def test_saving_service_does_not_cause_deletion_of_services_for_other_organizations(self):
        pass

    def test_that_a_changed_service_under_a_location_keeps_the_taskservicesimilarity_unchangeds(self):
        organization = OrganizationBuilder().create()
        location = LocationBuilder(organization).create()
        service = ServiceBuilder(organization).with_location(location).create()

        task_id = a_string()
        Task(id=task_id, name=a_string(), description=a_string()).save()
        set_service_similarity_score(task_id, service.id, a_float())

        self.assertEqual(len(TaskServiceSimilarityScore.objects.all()), 1)

        new_service = (ServiceBuilder(organization).
                       with_id(service.id).
                       with_location(location).
                       build_dto())
        new_location = (LocationBuilder(organization).
                        with_id(location.id).
                        with_services([new_service]).
                        build_dto())
        new_organization = (OrganizationBuilder().
                            with_id(organization.id).
                            with_locations([new_location]).
                            build_dto())
        save_organization_with_locations_and_services(new_organization, {}, ImportCounters())

        self.assertEqual(len(TaskServiceSimilarityScore.objects.all()), 1)
        self.assertEqual(TaskServiceSimilarityScore.objects.all()[0].service_id, service.id)

    def test_that_a_removed_service_under_a_location_causes_taskservicesimilarity_to_be_deleted(self):
        organization = OrganizationBuilder().create()
        location = LocationBuilder(organization).create()
        service = ServiceBuilder(organization).with_location(location).create()

        task_id = a_string()
        Task(id=task_id, name=a_string(), description=a_string()).save()
        set_service_similarity_score(task_id, service.id, a_float())

        self.assertEqual(len(TaskServiceSimilarityScore.objects.all()), 1)

        location_without_service = LocationBuilder(organization).with_id(location.id).build_dto()
        new_organization = (OrganizationBuilder().
                            with_id(organization.id).
                            with_locations([location_without_service]).
                            build_dto())
        save_organization_with_locations_and_services(new_organization, {}, ImportCounters())

        self.assertEqual(len(TaskServiceSimilarityScore.objects.all()), 0)

    def test_that_changes_to_service_taxonomy_terms_are_saved(self):
        organization = OrganizationBuilder().create()
        location = LocationBuilder(organization).create()
        taxonomy_term = TaxonomyTermBuilder().create()
        service = (ServiceBuilder(organization).
                   with_location(location).
                   with_taxonomy_terms([taxonomy_term]).
                   create())

        new_taxonomy_term = TaxonomyTermBuilder().create()
        new_service = (ServiceBuilder(organization).
                       with_location(location).
                       with_taxonomy_terms([new_taxonomy_term]).
                       build_dto())
        new_location = (LocationBuilder(organization).
                        with_id(location.id).
                        with_services([new_service]).
                        build_dto())
        new_organization = (OrganizationBuilder().
                            with_id(organization.id).
                            with_locations([new_location]).
                            build_dto())

        save_organization_with_locations_and_services(new_organization, {}, ImportCounters())

        self.assertEqual(len(Service.objects.all()), 1)
        all_services = Service.objects.all()
        self.assertEqual(all_services[0].taxonomy_terms.all()[0].taxonomy_id, new_taxonomy_term.taxonomy_id)

    def test_that_a_changed_service_under_a_location_causes_taxonomy_term_to_be_deleted(self):
        organization = OrganizationBuilder().create()
        location = LocationBuilder(organization).create()
        term = TaxonomyTermBuilder().create()
        service = (ServiceBuilder(organization).
                   with_location(location).
                   with_taxonomy_terms([term]).
                   create())
        self.assertEqual((Service.objects.
                          filter(pk=service.id).all()[0].
                          taxonomy_terms.all()[0].
                          taxonomy_id), term.taxonomy_id)

        new_service_without_taxonomy_term = (ServiceBuilder(organization).
                                             with_id(service.id).
                                             with_location(location).
                                             build_dto())
        new_location = (LocationBuilder(organization).
                        with_id(location.id).
                        with_services([new_service_without_taxonomy_term]).
                        build_dto())
        new_organization = (OrganizationBuilder().
                            with_id(organization.id).
                            with_locations([new_location]).
                            build_dto())

        save_organization_with_locations_and_services(new_organization, {}, ImportCounters())

        self.assertEqual(len(Service.objects.filter(pk=service.id).all()[0].taxonomy_terms.all()), 0)

    def test_that_a_removed_service_under_a_location_causes_taxonomy_term_to_be_deleted(self):
        pass



class LocationPropertiesTests(TestCase):
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

    def test_that_changed_phone_number_under_location_is_updated(self):
        location = LocationBuilder(self.organization). with_id(self.location_id). create()
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

    def test_that_changed_physical_address_under_location_is_updated(self):
        old_address = AddressBuilder().with_location_id(self.location_id).create()
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

    def test_that_changed_postal_address_under_location_is_updated(self):
        old_address = (AddressBuilder().
                       with_location_id(self.location_id).
                       create())
        location = (LocationBuilder(self.organization).
                    with_id(self.location_id).
                    with_postal_address(old_address).
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

    def test_that_new_address_under_location_creates_record(self):
        address = (AddressBuilder().
                   with_location_id(self.location_id).
                   with_address_type('postal_address').
                   build_dto())
        location = LocationBuilder(self.organization).with_postal_address(address).build_dto()

        save_locations([location], self.organization.id, {}, ImportCounters())
        self.assertEqual(len(Address.objects.all()), 1)

    def test_that_new_phone_number_under_location_creates_record(self):
        phone_at_location_dto = dtos.PhoneAtLocation(phone_number_type_id=self.phone_number_type_id,
                                                     phone_number=a_phone_number(),
                                                     location_id=self.location_id)
        location_dto = (LocationBuilder(self.organization).
                        with_id(self.location_id).
                        with_phone_numbers([phone_at_location_dto]).
                        build_dto())
        save_locations([location_dto], self.organization.id, {}, ImportCounters())
        self.assertEqual(len(PhoneAtLocation.objects.all()), 1)

    def test_that_address_under_newly_absent_location_is_removed(self):
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

    def test_that_phone_number_under_newly_absent_location_is_removed(self):
        location = (LocationBuilder(self.organization). create())
        PhoneAtLocation.objects.create(phone_number_type=self.phone_number_type,
                                       phone_number=a_phone_number(),
                                       location=location)
        self.assertEqual(len(PhoneAtLocation.objects.all()), 1)

        second_location = LocationBuilder(self.organization).build_dto()

        save_locations([second_location], self.organization.id, {}, ImportCounters())

        self.assertEqual(len(PhoneAtLocation.objects.all()), 0)
