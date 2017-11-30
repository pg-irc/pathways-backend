from bc211 import parser
from organizations.models import Organization
from service_providers.models import ServiceProvider
from django.utils import translation

def read_records_from_file(file):
    xml = file.read()
    return parser.parse(xml)

def save_records_to_database(records):
    translation.activate('en')

    number_of_organizations = save_organizations(records.organizations)
    number_of_service_providers = save_service_providers(records.service_providers)

    return {
        'number_of_organizations': number_of_organizations,
        'number_of_service_providers': number_of_service_providers,
    }

def save_organizations(records):
    count = 0
    for record in records:
        active_record = build_organization_active_record(record)
        active_record.save()
        count += 1
    return count

def build_organization_active_record(record):
    active_record = Organization()
    active_record.id = record.id
    active_record.name = record.name
    active_record.description = record.description
    active_record.website = record.website
    active_record.email = record.email
    return active_record

def save_service_providers(records):
    count = 0
    for record in records:
        active_record = build_service_provider_active_record(record)
        active_record.save()
        count += 1
    return count

def build_service_provider_active_record(record):
    active_record = ServiceProvider()
    active_record.name = record.name
    has_location = record.spatial_location is not None
    active_record.latitude = record.spatial_location.latitude if has_location else None
    active_record.longitude = record.spatial_location.longitude if has_location else None
    active_record.description = record.description
    return active_record
