from django.db import connection
from django.test import TestCase
from django.utils import translation
from bc211 import dtos
from bc211.importer import update_entire_organization, update_all_organizations
from bc211.location import update_locations
from bc211.import_counters import ImportCounters
from human_services.addresses.models import Address, AddressType
from human_services.addresses.tests.helpers import AddressBuilder
from human_services.organizations.tests.helpers import OrganizationBuilder
from human_services.locations.models import Location, LocationAddress, ServiceAtLocation
from human_services.locations.tests.helpers import LocationBuilder
from human_services.phone_at_location.models import PhoneAtLocation, PhoneNumberType
from human_services.services.models import Service
from human_services.services.tests.helpers import ServiceBuilder
from human_services.services_at_location.tests.helpers import set_service_similarity_score
from common.testhelpers.random_test_values import a_phone_number, a_string, a_float
from search.models import Task, TaskServiceSimilarityScore
from taxonomies.tests.helpers import TaxonomyTermBuilder
import xml.etree.ElementTree as etree


translation.activate('en')


class UpdateOrganizationTests(TestCase):

    def test_can_create_an_organization(self):
        BASELINE = 'bc211/data/BC211_data_excerpt.xml'
        nodes = etree.iterparse(BASELINE, events=('end',))
        update_all_organizations(nodes, {}, ImportCounters())

        counters = ImportCounters()
        FILE_WITH_MISSING_ORG = 'bc211/data/BC211_data_excerpt_with_one_more_organization.xml'
        nodes = etree.iterparse(FILE_WITH_MISSING_ORG, events=('end',))
        update_all_organizations(nodes, {}, counters)

        self.assertEqual(counters.organizations_created, 1)

    def test_can_update_an_organization(self):
        BASELINE = 'bc211/data/BC211_data_excerpt.xml'
        nodes = etree.iterparse(BASELINE, events=('end',))
        update_all_organizations(nodes, {}, ImportCounters())

        counters = ImportCounters()
        FILE_WITH_MISSING_ORG = 'bc211/data/BC211_data_excerpt_with_one_changed_organization.xml'
        nodes = etree.iterparse(FILE_WITH_MISSING_ORG, events=('end',))
        update_all_organizations(nodes, {}, counters)

        self.assertEqual(counters.organizations_updated, 1)


class LocationsUnderOrganizationTests(TestCase):

    def test_that_new_location_under_organization_creates_record(self):
        organization = OrganizationBuilder().create()

        location = LocationBuilder(organization).build_dto()
        organization_with_location = (OrganizationBuilder().
                                      with_id(organization.id).
                                      with_locations([location]).
                                      build_dto())

        update_entire_organization(organization_with_location, {}, ImportCounters())

        locations = Location.objects.all()
        self.assertEqual(len(locations), 1)
        self.assertEqual(locations[0].id, location.id)

    def test_that_changed_location_under_organization_is_updated(self):
        organization = OrganizationBuilder().create()
        location_id = a_string()
        LocationBuilder(organization).with_id(location_id).create()
        new_location_dto = (LocationBuilder(organization).
                            with_id(location_id).
                            build_dto())

        update_locations([new_location_dto], organization.id, {}, ImportCounters())

        all_locations = Location.objects.all()
        self.assertEqual(len(all_locations), 1)
        self.assertEqual(all_locations[0].id, location_id)
        self.assertEqual(all_locations[0].name, new_location_dto.name)

    def test_that_location_with_added_address_is_updated(self):
        organization = OrganizationBuilder().create()
        location_id = a_string()
        builder = LocationBuilder(organization).with_id(location_id)
        builder.create()

        the_city = a_string()
        address_dto = (AddressBuilder().
                       with_city(the_city).
                       with_location_id(location_id).
                       with_address_type('physical_address').
                       build_dto())
        location_dto = builder.with_physical_address(address_dto).build_dto()

        update_locations([location_dto], organization.id, {}, ImportCounters())

        location_addresses = LocationAddress.objects.filter(location_id=location_id).all()
        self.assertEqual(len(location_addresses), 1)
        addresses = Address.objects.filter(id=location_addresses[0].address_id).all()
        self.assertEqual(len(addresses), 1)
        self.assertEqual(addresses[0].city, the_city)

    def test_that_locations_with_added_phone_number_is_updated(self):
        organization = OrganizationBuilder().create()
        location_builder = LocationBuilder(organization)
        location = location_builder.create()

        phone_number = a_phone_number()
        phone_number_type = a_string()
        new_phone_at_location_dto = dtos.PhoneAtLocation(phone_number_type_id=phone_number_type,
                                                         phone_number=phone_number,
                                                         location_id=location.id)

        location_dto = location_builder.with_phone_numbers([new_phone_at_location_dto]).build_dto()
        update_locations([location_dto], organization.id, {}, ImportCounters())

        phones_at_location = PhoneAtLocation.objects.filter(location_id=location.id).all()
        self.assertEqual(len(phones_at_location), 1)
        self.assertEqual(phones_at_location[0].phone_number, phone_number)
        self.assertEqual(phones_at_location[0].phone_number_type.id, phone_number_type)


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
        update_entire_organization(new_organization_dto, {}, ImportCounters())

        services = Service.objects.all()
        self.assertEqual(len(services), 1)
        self.assertEqual(services[0].id, service_dto.id)

        sal = ServiceAtLocation.objects.all()
        self.assertEqual(len(sal), 1)
        self.assertEqual(sal[0].location.id, location_dto.id)
        self.assertEqual(sal[0].service.id, service_dto.id)

    def test_that_changed_service_under_location_is_updated(self):
        organization = OrganizationBuilder().create()
        location = LocationBuilder(organization).create()
        service = ServiceBuilder(organization).with_location(location).create()

        new_service = ServiceBuilder(organization).with_id(service.id).with_location(location).build_dto()
        new_location = LocationBuilder(organization).with_id(location.id).with_services([new_service]).build_dto()
        new_organization = OrganizationBuilder().with_id(organization.id).with_locations([new_location]).build_dto()

        update_entire_organization(new_organization, {}, ImportCounters())

        self.assertEqual(len(Service.objects.all()), 1)
        self.assertEqual(Service.objects.all()[0].name, new_service.name)

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
        update_entire_organization(new_organization, {}, ImportCounters())

        self.assertEqual(len(TaskServiceSimilarityScore.objects.all()), 1)
        self.assertEqual(TaskServiceSimilarityScore.objects.all()[0].service_id, service.id)

    def get_all_service_taxonomy_terms(self):
        with connection.cursor() as cursor:
            cursor.execute('select * from services_service_taxonomy_terms')
            return cursor.fetchall()


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

    def test_that_new_address_under_location_creates_record(self):
        address = (AddressBuilder().
                   with_location_id(self.location_id).
                   with_address_type('postal_address').
                   build_dto())
        location = LocationBuilder(self.organization).with_postal_address(address).build_dto()

        update_locations([location], self.organization.id, {}, ImportCounters())
        self.assertEqual(len(Address.objects.all()), 1)

    def test_that_new_phone_number_under_location_creates_record(self):
        phone_at_location_dto = dtos.PhoneAtLocation(phone_number_type_id=self.phone_number_type_id,
                                                     phone_number=a_phone_number(),
                                                     location_id=self.location_id)
        location_dto = (LocationBuilder(self.organization).
                        with_id(self.location_id).
                        with_phone_numbers([phone_at_location_dto]).
                        build_dto())
        update_locations([location_dto], self.organization.id, {}, ImportCounters())
        self.assertEqual(len(PhoneAtLocation.objects.all()), 1)


class ImportCountTests(TestCase):
    def test_that_a_new_organization_is_counted(self):
        organization = OrganizationBuilder().build_dto()
        counters = ImportCounters()

        update_entire_organization(organization, {}, counters)

        self.assertEqual(counters.organizations_created, 1)
        self.assertEqual(counters.organizations_updated, 0)

    def test_that_a_new_location_is_counted(self):
        organization = OrganizationBuilder().create()

        location_dto = (LocationBuilder(organization).
                        build_dto())
        new_organization_dto = (OrganizationBuilder().
                                with_id(organization.id).
                                with_locations([location_dto]).
                                build_dto())
        counters = ImportCounters()

        update_entire_organization(new_organization_dto, {}, counters)

        self.assertEqual(counters.locations_created, 1)
        self.assertEqual(counters.locations_updated, 0)

    def test_that_a_new_service_is_counted(self):
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
        counters = ImportCounters()
        update_entire_organization(new_organization_dto, {}, counters)
        self.assertEqual(counters.services_created, 1)

    def test_that_a_updated_organization_is_counted(self):
        organization_builder = OrganizationBuilder()
        organization_builder.create()

        new_organization_dto = organization_builder.with_name(a_string()).build_dto()

        counters = ImportCounters()

        update_entire_organization(new_organization_dto, {}, counters)

        self.assertEqual(counters.organizations_created, 0)
        self.assertEqual(counters.organizations_updated, 1)

    def test_that_a_updated_location_is_counted(self):
        organization_builder = OrganizationBuilder()
        organization = organization_builder.create()
        location_builder = LocationBuilder(organization)
        location_builder.create()
        new_location_dto = location_builder.with_name(a_string()).build_dto()
        new_organization_dto = organization_builder.with_locations([new_location_dto]).build_dto()
        counters = ImportCounters()

        update_entire_organization(new_organization_dto, {}, counters)

        self.assertEqual(counters.locations_updated, 1)
        self.assertEqual(counters.locations_created, 0)

    def test_that_a_updated_service_is_counted(self):
        organization_builder = OrganizationBuilder()
        organization = organization_builder.create()
        location_builder = LocationBuilder(organization)
        location = location_builder.create()
        service_builder = ServiceBuilder(organization).with_location(location)
        service_builder.create()

        changed_service = service_builder.with_name(a_string()).build_dto()
        new_location = location_builder.with_services([changed_service]).build_dto()
        new_organization = organization_builder.with_locations([new_location]).build_dto()

        counters = ImportCounters()
        update_entire_organization(new_organization, {}, counters)

        self.assertEqual(counters.services_updated, 1)
        self.assertEqual(counters.services_created, 0)

    def test_that_an_service_with_changed_taxonomy_term_is_counted_as_updated(self):
        organization_builder = OrganizationBuilder()
        organization = organization_builder.create()
        location_builder = LocationBuilder(organization)
        location = location_builder.create()
        first_taxonomy_term = TaxonomyTermBuilder().create()
        service_builder = ServiceBuilder(organization).with_location(location).with_taxonomy_terms([first_taxonomy_term])
        service_builder.create()

        second_taxonomy_term = TaxonomyTermBuilder().create()
        service_dto = service_builder.with_taxonomy_terms([second_taxonomy_term]).build_dto()
        location_dto = location_builder.with_services([service_dto]).build_dto()
        organization_dto = organization_builder.with_locations([location_dto]).build_dto()

        counters = ImportCounters()
        update_entire_organization(organization_dto, {}, counters)

        self.assertEqual(counters.services_updated, 1)
        self.assertEqual(counters.services_created, 0)

    def test_that_an_unchanged_organization_is_not_counted_as_updated(self):
        organization_builder = OrganizationBuilder()
        organization_builder.create()

        new_organization_dt = organization_builder.build_dto()

        counters = ImportCounters()

        update_entire_organization(new_organization_dt, {}, counters)

        self.assertEqual(counters.organizations_updated, 0)
        self.assertEqual(counters.organizations_created, 0)

    def test_that_an_unchanged_location_is_not_counted_as_updated(self):
        organization = OrganizationBuilder().create()
        location_id = a_string()
        location_builder = LocationBuilder(organization).with_id(location_id)
        location_builder.create()

        new_location_dto = location_builder.build_dto()
        new_organization_dto = (OrganizationBuilder().
                                with_id(organization.id).
                                with_locations([new_location_dto]).
                                build_dto())
        counters = ImportCounters()

        update_entire_organization(new_organization_dto, {}, counters)

        self.assertEqual(counters.locations_updated, 0)

    def test_that_an_unchanged_location_with_addresses_is_not_counted_as_updated(self):
        organization = OrganizationBuilder().create()
        location_id = a_string()
        postal_address_builder = (AddressBuilder().
                                  with_location_id(location_id).
                                  with_address_type('physical_address'))
        physical_address_builder = (AddressBuilder().
                                    with_location_id(location_id).
                                    with_address_type('physical_address'))
        location_builder = (LocationBuilder(organization).
                            with_id(location_id).
                            with_physical_address(physical_address_builder.build_dto()).
                            with_postal_address(postal_address_builder.build_dto()))
        location = location_builder.create()

        postal_address = postal_address_builder.create()
        physical_address = physical_address_builder.create()

        LocationAddress(address=postal_address, location=location, address_type_id='postal_address').save()
        LocationAddress(address=physical_address, location=location, address_type_id='physical_address').save()

        new_location_dto = location_builder.build_dto()
        new_organization_dto = (OrganizationBuilder().
                                with_id(organization.id).
                                with_locations([new_location_dto]).
                                build_dto())
        counters = ImportCounters()

        update_entire_organization(new_organization_dto, {}, counters)

        self.assertEqual(counters.locations_updated, 0)

    def test_that_an_unchanged_location_with_phone_number_is_not_counted_as_updated(self):
        organization = OrganizationBuilder().create()
        location_id = a_string()
        location_builder = LocationBuilder(organization).with_id(location_id)
        location = location_builder.create()

        phone_number = a_phone_number()
        phone_type_id = a_string()
        phone_type = PhoneNumberType.objects.create(id=phone_type_id)
        PhoneAtLocation.objects.create(phone_number_type=phone_type, phone_number=phone_number, location=location)
        phone_at_location_dto = dtos.PhoneAtLocation(phone_number_type_id=phone_type_id,
                                                     phone_number=phone_number,
                                                     location_id=location_id)

        new_location_dto = location_builder.with_phone_numbers([phone_at_location_dto]).build_dto()
        new_organization_dto = (OrganizationBuilder().
                                with_id(organization.id).
                                with_locations([new_location_dto]).
                                build_dto())
        counters = ImportCounters()

        update_entire_organization(new_organization_dto, {}, counters)

        self.assertEqual(counters.locations_updated, 0)

    def test_that_an_unchanged_service_is_not_counted_as_updated(self):
        organization_builder = OrganizationBuilder()
        organization = organization_builder.create()
        location_builder = LocationBuilder(organization)
        location = location_builder.create()
        service_builder = ServiceBuilder(organization).with_location(location)
        service_builder.create()

        new_service = service_builder.build_dto()
        new_location = location_builder.with_services([new_service]).build_dto()
        new_organization = organization_builder.with_locations([new_location]).build_dto()

        counters = ImportCounters()
        update_entire_organization(new_organization, {}, counters)

        self.assertEqual(counters.services_updated, 0)
        self.assertEqual(counters.services_created, 0)

    def test_that_an_unchanged_service_with_taxonomy_term_is_not_counted_as_updated(self):
        organization_builder = OrganizationBuilder()
        organization = organization_builder.create()
        location_builder = LocationBuilder(organization)
        location = location_builder.create()
        taxonomy_terms = TaxonomyTermBuilder().create_many()
        service_builder = ServiceBuilder(organization).with_location(location).with_taxonomy_terms(taxonomy_terms)
        service = service_builder.create()

        service_dto = service_builder.build_dto()
        location_dto = location_builder.with_services([service_dto]).build_dto()
        organization_dto = organization_builder.with_locations([location_dto]).build_dto()

        counters = ImportCounters()
        update_entire_organization(organization_dto, {}, counters)

        self.assertEqual(counters.services_updated, 0)
        self.assertEqual(counters.services_created, 0)

    def test_that_a_location_with_changed_name_is_counted_as_updated(self):
        organization = OrganizationBuilder().create()
        location_builder = LocationBuilder(organization)
        location_builder.create()

        new_location_dto = location_builder.with_name(a_string()).build_dto()
        new_organization_dto = (OrganizationBuilder().
                                with_id(organization.id).
                                with_locations([new_location_dto]).
                                build_dto())
        counters = ImportCounters()

        update_entire_organization(new_organization_dto, {}, counters)

        self.assertEqual(counters.locations_updated, 1)

    def set_physical_address(self, location, address):
        physical_address_type = AddressType.objects.get(pk='physical_address')
        LocationAddress(address=address, location=location,
                        address_type=physical_address_type).save()
