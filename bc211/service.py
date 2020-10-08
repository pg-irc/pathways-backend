import logging
from bc211.taxonomy import save_service_taxonomy_terms
from bc211.is_inactive import is_inactive
from human_services.services.models import Service
from search.models import TaskServiceSimilarityScore
from human_services.locations.models import ServiceAtLocation

LOGGER = logging.getLogger(__name__)


def build_service_active_record(record):
    active_record = get_or_create_service_active_record(record.id)
    active_record.name = record.name
    active_record.organization_id = record.organization_id
    active_record.description = record.description
    return active_record


def get_or_create_service_active_record(pk):
    if Service.objects.filter(id=pk).exists():
        return Service.objects.get(id=pk)
    record = Service()
    record.id = pk
    return record


def build_service_at_location_active_record(record):
    active_record = ServiceAtLocation()
    active_record.service_id = record.id
    active_record.location_id = record.site_id
    return active_record


def update_services_for_location(location_id, services, counters):
    for service in services:
        save_service_if_needed(service, counters)


def save_service_if_needed(service, counters):
    if is_inactive(service):
        return
    existing = get_existing_service_or_none(service)
    if not existing:
        active_record = build_service_active_record(service)
        active_record.save()
        counters.count_service()
        LOGGER.debug('created service "%s" "%s"', service.id, service.name)
        save_service_at_location(service)
        save_service_taxonomy_terms(service.taxonomy_terms, active_record, counters)
    else:
        LOGGER.warn('duplicate service "%s" "%s"', service.id, service.name)


def get_existing_service_or_none(service):
    pk = service.id
    if Service.objects.filter(id=pk).exists():
        return Service.objects.get(id=pk)
    return None


def service_already_exists(service):
    return Service.objects.filter(pk=service.id).exists()


def save_service_at_location(service):
    active_record = build_service_at_location_active_record(service)
    active_record.save()
    LOGGER.debug('created service at location: %s %s', service.id, service.site_id)
