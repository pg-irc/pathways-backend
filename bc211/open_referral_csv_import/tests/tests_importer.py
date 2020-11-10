import unittest
import string
from django.test import TestCase
from bc211.open_referral_csv_import.organization import import_organizations_file, import_organization
from bc211.open_referral_csv_import.service import import_services_file, import_service
from ..location import import_locations_file, save_location
from ..service_at_location import import_services_at_location_file, save_service_at_location
from ..address import import_addresses_file, save_address, save_location_address
from .helpers import (OpenReferralCsvOrganizationBuilder, OpenReferralCsvServiceBuilder,
                        OpenReferralCsvLocationBuilder, OpenReferralCsvServiceAtLocationBuilder, OpenReferralCsvAddressBuilder)
from common.testhelpers.random_test_values import (a_string, an_email_address, a_website_address,
                                                    a_latitude_as_a_string, a_longitude_as_a_string)
from human_services.organizations.models import Organization
from human_services.organizations.tests.helpers import OrganizationBuilder
from human_services.services.tests.helpers import ServiceBuilder
from human_services.locations.tests.helpers import LocationBuilder
from human_services.services.models import Service
from human_services.locations.models import Location, ServiceAtLocation
from human_services.addresses.models import Address, AddressType
from human_services.locations.models import LocationAddress
from django.contrib.gis.geos import Point


class OpenReferralOrganizationImporterTests(TestCase):
    def test_can_import_id(self):
        the_id = a_string()
        organization_data = OpenReferralCsvOrganizationBuilder().with_id(the_id).build()
        import_organization(organization_data)
        organizations = Organization.objects.all()
        self.assertEqual(organizations[0].id, the_id)
    
    def test_can_import_name(self):
        the_name = a_string()
        organization_data = OpenReferralCsvOrganizationBuilder().with_name(the_name).build()
        import_organization(organization_data)
        organizations = Organization.objects.all()
        self.assertEqual(organizations[0].name, the_name)

    def test_can_import_alternate_name(self):
        the_alternate_name = a_string()
        organization_data = OpenReferralCsvOrganizationBuilder().with_alternate_name(the_alternate_name).build()
        import_organization(organization_data)
        organizations = Organization.objects.all()
        self.assertEqual(organizations[0].alternate_name, the_alternate_name)

    def test_can_import_description(self):
        the_description = a_string()
        organization_data = OpenReferralCsvOrganizationBuilder().with_description(the_description).build()
        import_organization(organization_data)
        organizations = Organization.objects.all()
        self.assertEqual(organizations[0].description, the_description)

    def test_can_import_email(self):
        the_email = an_email_address()
        organization_data = OpenReferralCsvOrganizationBuilder().with_email(the_email).build()
        import_organization(organization_data)
        organizations = Organization.objects.all()
        self.assertEqual(organizations[0].email, the_email)

    def test_can_import_website(self):
        the_website = a_website_address()
        organization_data = OpenReferralCsvOrganizationBuilder().with_url(the_website).build()
        import_organization(organization_data)
        organizations = Organization.objects.all()
        self.assertEqual(organizations[0].website, the_website)


class OpenReferralServiceImporterTests(TestCase):
    def setUp(self):
        self.organization_id_passed_to_organization_builder = a_string()
        self.organization = OrganizationBuilder().with_id(self.organization_id_passed_to_organization_builder).build()
        self.organization.save()
    
    def test_can_import_id(self): 
        the_id = a_string()
        service_data = OpenReferralCsvServiceBuilder(self.organization).with_id(the_id).build()
        import_service(service_data)
        services = Service.objects.all()
        self.assertEqual(services[0].id, the_id)

    def test_can_import_organization_id(self):
        service_data = OpenReferralCsvServiceBuilder(self.organization).build()
        import_service(service_data)
        services = Service.objects.all()
        self.assertEqual(services[0].organization_id, self.organization_id_passed_to_organization_builder)
    
    def test_can_import_name(self):
        the_name = a_string()
        service_data = OpenReferralCsvServiceBuilder(self.organization).with_name(the_name).build()
        import_service(service_data)
        services = Service.objects.all()
        self.assertEqual(services[0].name, the_name)
    
    def test_can_import_alternate_name(self):
        the_alternate_name = a_string()
        service_data = OpenReferralCsvServiceBuilder(self.organization).with_alternate_name(the_alternate_name).build()
        import_service(service_data)
        services = Service.objects.all()
        self.assertEqual(services[0].alternate_name, the_alternate_name)

    def test_can_import_description(self):
        the_description = a_string()
        service_data = OpenReferralCsvServiceBuilder(self.organization).with_description(the_description).build()
        import_service(service_data)
        services = Service.objects.all()
        self.assertEqual(services[0].description, the_description)
    
    def test_can_import_website(self):
        the_website = a_website_address()
        service_data = OpenReferralCsvServiceBuilder(self.organization).with_url(the_website).build()
        import_service(service_data)
        services = Service.objects.all()
        self.assertEqual(services[0].website, the_website)

    def test_can_import_email(self):
        the_email = an_email_address()
        service_data = OpenReferralCsvServiceBuilder(self.organization).with_email(the_email).build()
        import_service(service_data)
        services = Service.objects.all()
        self.assertEqual(services[0].email, the_email)


class OpenReferralLocationImporterTests(TestCase):
    def setUp(self):
        self.organization_id_passed_to_organization_builder = a_string()
        self.organization = OrganizationBuilder().with_id(self.organization_id_passed_to_organization_builder).build()
        self.organization.save()
    
    def test_can_import_id(self):
        the_id = a_string()
        location_dto = OpenReferralCsvLocationBuilder(self.organization).with_id(the_id).build_dto()
        save_location(location_dto)
        locations = Location.objects.all()
        self.assertEqual(locations[0].id, the_id)
    
    def test_can_import_organization_id(self):
        location_dto = OpenReferralCsvLocationBuilder(self.organization).build_dto()
        save_location(location_dto)
        locations = Location.objects.all()
        self.assertEqual(locations[0].organization_id, self.organization_id_passed_to_organization_builder)
    
    def test_can_import_name(self):
        the_name = a_string()
        location_dto = OpenReferralCsvLocationBuilder(self.organization).with_name(the_name).build_dto()
        save_location(location_dto)
        locations = Location.objects.all()
        self.assertEqual(locations[0].name, the_name)

    def test_can_import_alternate_name(self):
        the_alternate_name = a_string()
        location_dto = OpenReferralCsvLocationBuilder(self.organization).with_alternate_name(the_alternate_name).build_dto()
        save_location(location_dto)
        locations = Location.objects.all()
        self.assertEqual(locations[0].alternate_name, the_alternate_name)

    def test_can_import_description(self):
        the_description = a_string()
        location_dto = OpenReferralCsvLocationBuilder(self.organization).with_description(the_description).build_dto()
        save_location(location_dto)
        locations = Location.objects.all()
        self.assertEqual(locations[0].description, the_description)
    
    def test_can_import_point(self):
        the_latitude = a_latitude_as_a_string()
        the_longitude = a_longitude_as_a_string()
        location_dto = OpenReferralCsvLocationBuilder(self.organization).with_latitude(the_latitude).with_longitude(the_longitude).build_dto()
        save_location(location_dto)
        locations = Location.objects.all()
        self.assertEqual(locations[0].point.x, location_dto.spatial_location.longitude)
        self.assertEqual(locations[0].point.y, location_dto.spatial_location.latitude)


class OpenReferralServiceAtLocationImporterTests(TestCase):
    def setUp(self):
        organization = OrganizationBuilder().build()
        organization.save()
        self.service_id_passed_to_service_builder = a_string()
        self.location_id_passed_to_location_builder = a_string()
        self.service = ServiceBuilder(organization).with_id(self.service_id_passed_to_service_builder).build()
        self.location = LocationBuilder(organization).with_id(self.location_id_passed_to_location_builder).build()
        self.service.save()
        self.location.save()
    
    def test_can_import_service_id(self):
        service_at_location_dto = OpenReferralCsvServiceAtLocationBuilder(self.service, self.location).build_dto()
        save_service_at_location(service_at_location_dto)
        services_at_location = ServiceAtLocation.objects.all()
        self.assertEqual(services_at_location[0].service_id, self.service_id_passed_to_service_builder)
    
    def test_can_import_location_id(self):
        service_at_location_dto = OpenReferralCsvServiceAtLocationBuilder(self.service, self.location).build_dto()
        save_service_at_location(service_at_location_dto)
        services_at_location = ServiceAtLocation.objects.all()
        self.assertEqual(services_at_location[0].location_id, self.location_id_passed_to_location_builder)


class OpenReferralAddressImporterTests(TestCase):
    def setUp(self):
        organization = OrganizationBuilder().build()
        organization.save()
        self.location_id_passed_to_location_builder = a_string()
        self.location = LocationBuilder(organization).with_id(self.location_id_passed_to_location_builder).build()
        self.location.save()
    
    def test_can_import_city(self):
        the_city = a_string()
        address_dto = OpenReferralCsvAddressBuilder(self.location).with_city(the_city).build_dto()
        save_address(address_dto)
        addresses = Address.objects.all()
        self.assertEqual(addresses[0].city, the_city)

    def test_can_import_country(self):
        the_country = a_string(2, string.ascii_uppercase)
        address_dto = OpenReferralCsvAddressBuilder(self.location).with_country(the_country).build_dto()
        save_address(address_dto)
        addresses = Address.objects.all()
        self.assertEqual(addresses[0].country, the_country)
    
    def test_can_import_attention(self):
        the_attention = a_string()
        address_dto = OpenReferralCsvAddressBuilder(self.location).with_attention(the_attention).build_dto()
        save_address(address_dto)
        addresses = Address.objects.all()
        self.assertEqual(addresses[0].attention, the_attention)
    
    def test_can_import_address(self):
        the_address = a_string()
        address_dto = OpenReferralCsvAddressBuilder(self.location).with_address(the_address).build_dto()
        save_address(address_dto)
        addresses = Address.objects.all()
        self.assertEqual(addresses[0].address, the_address)
    
    def test_can_import_state_province(self):
        the_state_province = a_string()
        address_dto = OpenReferralCsvAddressBuilder(self.location).with_state_province(the_state_province).build_dto()
        save_address(address_dto)
        addresses = Address.objects.all()
        self.assertEqual(addresses[0].state_province, the_state_province)

    def test_can_import_postal_code(self):
        the_postal_code = a_string()
        address_dto = OpenReferralCsvAddressBuilder(self.location).with_postal_code(the_postal_code).build_dto()
        save_address(address_dto)
        addresses = Address.objects.all()
        self.assertEqual(addresses[0].postal_code, the_postal_code)

class OpenReferralLocationAddressImporterTests(TestCase):
    def setUp(self):
        organization = OrganizationBuilder().build()
        organization.save()
        self.location_id_passed_to_location_builder = a_string()
        self.location = LocationBuilder(organization).with_id(self.location_id_passed_to_location_builder).build()
        self.location.save()
    
    def test_can_import_address_id(self):
        address_dto = OpenReferralCsvAddressBuilder(self.location).build_dto()
        address = save_address(address_dto)
        save_location_address(address, address_dto)
        location_addresses = LocationAddress.objects.all()
        addresses = Address.objects.all()
        self.assertEqual(location_addresses[0].address_id, addresses[0].id)

    def test_can_import_location_id(self):
        address_dto = OpenReferralCsvAddressBuilder(self.location).build_dto()
        address = save_address(address_dto)
        save_location_address(address, address_dto)
        location_addresses = LocationAddress.objects.all()
        self.assertEqual(location_addresses[0].location_id, self.location_id_passed_to_location_builder)
    
    def test_can_import_address_type(self):
        the_address_type = 'postal_address'
        address_dto = OpenReferralCsvAddressBuilder(self.location).with_address_type(the_address_type).build_dto()
        address = save_address(address_dto)
        save_location_address(address, address_dto)
        location_addresses = LocationAddress.objects.all()
        the_address_type_instance = AddressType.objects.get(pk=the_address_type)
        self.assertEqual(location_addresses[0].address_type, the_address_type_instance)
