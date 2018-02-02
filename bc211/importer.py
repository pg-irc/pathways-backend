import logging
from django.utils import translation
from locations.models import Location, ServiceAtLocation, LocationAddress
from organizations.models import Organization
from services.models import Service
from taxonomies.models import TaxonomyTerm
from addresses.models import Address, AddressType

LOGGER = logging.getLogger(__name__)

class ImportCounters:
    def __init__(self):
        self.organization_count = 0
        self.location_count = 0
        self.service_count = 0
        self.taxonomy_term_count = 0
        self.address_count = 0

    def count_organization(self):
        self.organization_count += 1

    def count_location(self):
        self.location_count += 1

    def count_service(self):
        self.service_count += 1

    def count_taxonomy_term(self):
        self.taxonomy_term_count += 1

    def count_address(self):
        self.address_count += 1

def save_records_to_database(organizations):
    translation.activate('en')
    counters = ImportCounters()
    save_organizations(organizations, counters)
    return counters

def save_organizations(organizations, counters):
    for organization in organizations:
        active_record = build_organization_active_record(organization)
        active_record.save()
        counters.count_organization()
        LOGGER.info('Organization "%s" "%s"', organization.id, organization.name)
        save_locations(organization.locations, counters)

def build_organization_active_record(record):
    active_record = Organization()
    active_record.id = record.id
    active_record.name = record.name
    active_record.description = record.description
    active_record.website = record.website
    active_record.email = record.email
    return active_record

def save_locations(locations, counters):
    for location in locations:
        active_record = build_location_active_record(location)
        active_record.save()
        counters.count_location()
        LOGGER.info('Location "%s" "%s"', location.id, location.name)
        save_services(location.services, counters)
        if location.physical_address:
            create_address_for_location(active_record, location.physical_address, counters)
        if location.postal_address:
            create_address_for_location(active_record, location.postal_address, counters)

def build_location_active_record(record):
    active_record = Location()
    active_record.id = record.id
    active_record.name = record.name
    active_record.organization_id = record.organization_id
    has_location = record.spatial_location is not None
    active_record.latitude = record.spatial_location.latitude if has_location else None
    active_record.longitude = record.spatial_location.longitude if has_location else None
    active_record.description = record.description
    return active_record

def build_service_active_record(record):
    active_record = Service()
    active_record.id = record.id
    active_record.name = record.name
    active_record.organization_id = record.organization_id
    active_record.description = record.description
    return active_record

def build_service_at_location_active_record(record):
    active_record = ServiceAtLocation()
    active_record.service_id = record.id
    active_record.location_id = record.site_id
    return active_record

def save_services(services, counters):
    for service in services:
        active_record = build_service_active_record(service)
        active_record.save()
        counters.count_service()
        LOGGER.info('Service "%s" "%s"', service.id, service.name)
        save_service_at_location(service)
        save_service_taxonomy_terms(service.taxonomy_terms, active_record, counters)

def save_service_at_location(service):
    active_record = build_service_at_location_active_record(service)
    active_record.save()
    LOGGER.info('Imported service at location: %s %s', service.id, service.site_id)

def save_service_taxonomy_terms(taxonomy_terms, service_active_record, counters):
    for taxonomy_term in taxonomy_terms:
        taxonomy_term_active_record = create_taxonomy_term_active_record(
            taxonomy_term,
            counters
        )
        service_active_record.taxonomy_terms.add(taxonomy_term_active_record)
        LOGGER.info('Imported service taxonomy term')
    service_active_record.save()

def create_taxonomy_term_active_record(record, counters):
    taxonomy_term_active_record, created = TaxonomyTerm.objects.get_or_create(
        taxonomy_id=record.taxonomy_id,
        name=record.name
    )
    if created:
        counters.count_taxonomy_term()
        LOGGER.debug('Taxonomy term "%s" "%s"', record.taxonomy_id, record.name)
    return taxonomy_term_active_record

def create_address_for_location(location, address_dto, counters):
    address = create_address(address_dto, counters)
    address_type = AddressType.objects.get(pk=address_dto.address_type_id)
    create_location_address(
        location,
        address,
        address_type
    )

def create_address(address_dto, counters):
    active_record, created = Address.objects.get_or_create(
        address=address_dto.address_lines,
        city=address_dto.city,
        country=address_dto.country,
        state_province=address_dto.state_province,
        postal_code=address_dto.postal_code,
        attention=None
    )
    if created:
        counters.count_address()
        LOGGER.info('Imported address: %s %s', active_record.id, active_record.address)
    return active_record

def create_location_address(location, address, address_type):
    active_record = LocationAddress(address=address, location=location,
                                    address_type=address_type).save()
    LOGGER.info('Imported location address')
    return active_record
