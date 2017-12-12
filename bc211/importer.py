from django.utils import translation
from locations.models import Location
from organizations.models import Organization
from taxonomies.models import Taxonomy
import logging

LOGGER = logging.getLogger(__name__)

class ImportCounters:
    def __init__(self):
        self.organization_count = 0
        self.location_count = 0
        self.service_count = 0
        self.taxonomy_count = 0

    def count_organization(self):
        self.organization_count += 1

    def count_location(self):
        self.location_count += 1

    def count_service(self):
        self.service_count += 1

    def count_taxonomy(self):
        self.taxonomy_count += 1

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
        LOGGER.info('Imported organization: %s %s', organization.id, organization.name)
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
        LOGGER.info('Imported location: %s %s', location.id, location.name)
        save_services(location.services, counters)

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

def save_services(services, counters):
    for service in services:
        # Don't save services themselves for now.
        counters.count_service()
        save_taxonomies(service.taxonomies, counters)

def save_taxonomies(taxonomies, counters):
    for taxonomy in taxonomies:
        if save_taxonomy(taxonomy):
            counters.count_taxonomy()
            LOGGER.info('Imported taxonomy: %s %s', taxonomy.vocabulary, taxonomy.name)

def save_taxonomy(record):
    active_record, created = Taxonomy.objects.get_or_create(
        vocabulary=record.vocabulary,
        name=record.name
    )
    return created
