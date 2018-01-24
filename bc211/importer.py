import logging
from django.utils import translation
from django.core.exceptions import ValidationError
from locations.models import Location, ServiceAtLocation
from organizations.models import Organization
from services.models import Service
from taxonomies.models import TaxonomyTerm
from addresses.models import Address

LOGGER = logging.getLogger(__name__)

class ImportCounters:
    def __init__(self):
        self.organization_count = 0
        self.location_count = 0
        self.service_count = 0
        self.service_at_location_count = 0
        self.taxonomy_term_count = 0
        self.address_count = 0

    def count_organization(self):
        self.organization_count += 1

    def count_location(self):
        self.location_count += 1

    def count_service(self):
        self.service_count += 1

    def count_service_at_location(self):
        self.service_at_location_count += 1

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
        save_addresses(location.addresses, counters)

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
        save_service_at_location(service, counters)
        save_service_taxonomy_terms(service.taxonomy_terms, active_record, counters)

def save_service_at_location(service, counters):
    active_record = build_service_at_location_active_record(service)
    active_record.save()
    counters.count_service_at_location()
    LOGGER.info('Service at location "%s" "%s"', service.id, service.site_id)

def save_service_taxonomy_terms(taxonomy_terms, service_active_record, counters):
    for taxonomy_term in taxonomy_terms:
        taxonomy_term_active_record = create_taxonomy_term_active_record(
            taxonomy_term,
            counters
        )
        service_active_record.taxonomy_terms.add(taxonomy_term_active_record)
        LOGGER.debug('Taxonomy term "%s" added to service "%s"', taxonomy_term.name, service_active_record.name)
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

def save_addresses(addresses, counters):
    for address in addresses:
        active_record = create_address_active_record(address, counters)

def create_address_active_record(record, counters):
    active_record, created = Address.objects.get_or_create(
        address=record.address_lines,
        city=record.city,
        country=record.country,
        state_province=record.state_province,
        postal_code=record.postal_code
    )
    if created:
        counters.count_address()
        LOGGER.info('Imported address: %s %s', active_record.id, active_record.address)
    return active_record
