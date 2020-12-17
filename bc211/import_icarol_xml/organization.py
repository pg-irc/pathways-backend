import logging
from bc211.is_inactive import is_inactive
from bc211.import_icarol_xml.location import update_locations
from bc211.service import update_services_for_location
from django.utils import translation
from human_services.organizations.models import Organization

LOGGER = logging.getLogger(__name__)


def update_entire_organization(organization, city_latlong_map, counters):
    update_organization(organization, counters)
    locations = list(organization.locations)
    update_locations(locations, organization.id, city_latlong_map, counters)
    for location in locations:
        if not is_inactive(location.description):
            update_services_for_location(location.id, location.services, counters)


def update_organization(organization, counters):
    if is_inactive(organization.description):
        return
    translation.activate('en')
    existing = get_existing_organization_or_none(organization)
    if not existing:
        active_record = build_organization_active_record(organization)
        active_record.save()
        counters.count_organization_created()
        LOGGER.debug('created "%s" "%s"', organization.id, organization.name)
    else:
        LOGGER.warning('duplicate organization "%s" "%s"', organization.id, organization.name)


def get_existing_organization_or_none(organization):
    result = Organization.objects.filter(id=organization.id).all()
    return result[0] if result else None


def build_organization_active_record(record):
    active_record = get_or_create_organization_active_record(record.id)
    active_record.name = record.name
    active_record.description = record.description
    active_record.website = record.website
    active_record.email = record.email
    return active_record


def get_or_create_organization_active_record(pk):
    if Organization.objects.filter(id=pk).exists():
        return Organization.objects.get(id=pk)
    record = Organization()
    record.id = pk
    return record
