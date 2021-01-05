from django.db import connection
from django.test import TestCase
from django.utils import translation
from bc211.import_icarol_xml import dtos
from bc211.import_icarol_xml.importer import update_entire_organization, update_all_organizations
from bc211.import_icarol_xml.location import update_locations
from bc211.import_icarol_xml.import_counters import ImportCounters
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
        BASELINE = 'bc211/import_icarol_xml/tests/data/BC211_data_excerpt.xml'
        nodes = etree.iterparse(BASELINE, events=('end',))
        update_all_organizations(nodes, {}, ImportCounters())

        counters = ImportCounters()
        FILE_WITH_MISSING_ORG = 'bc211/import_icarol_xml/tests/data/BC211_data_excerpt_with_one_more_organization.xml'
        nodes = etree.iterparse(FILE_WITH_MISSING_ORG, events=('end',))
        update_all_organizations(nodes, {}, counters)

        self.assertEqual(counters.organizations_created, 1)


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

    def test_that_an_unchanged_organization_is_not_counted_as_updated(self):
        organization_builder = OrganizationBuilder()
        organization_builder.create()

        new_organization_dt = organization_builder.build_dto()

        counters = ImportCounters()

        update_entire_organization(new_organization_dt, {}, counters)

        self.assertEqual(counters.organizations_created, 0)
