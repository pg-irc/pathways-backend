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
        LOGGER.info('created "%s" "%s"', service.id, service.name)
        save_service_at_location(service)
        save_service_taxonomy_terms(service.taxonomy_terms, active_record, counters)
    elif not is_service_equal(existing, service):
        active_record = build_service_active_record(service)
        active_record.save()
        counters.count_services_updates()
        LOGGER.info('updated "%s" "%s"', service.id, service.name)
        save_service_at_location(service)
        save_service_taxonomy_terms(service.taxonomy_terms, active_record, counters)


def get_existing_service_or_none(service):
    pk = service.id
    if Service.objects.filter(id=pk).exists():
        return Service.objects.get(id=pk)
    return None


def is_service_equal(active_record, dto):
    ar_hash = hash(service_to_string(ArAdaptor(active_record)))
    dto_hash = hash(service_to_string(DtoAdapter(dto)))
    return ar_hash == dto_hash


class ArAdaptor:
    def __init__(self, service):
        self.service = service

    def the_id(self):
        return self.service.id

    def name(self):
        return self.service.name

    def description(self):
        return self.service.description

    def taxonomy_terms(self):
        return self.service.taxonomy_terms.all()


class DtoAdapter:
    def __init__(self, service):
        self.service = service

    def the_id(self):
        return self.service.id

    def name(self):
        return self.service.name

    def description(self):
        return self.service.description

    def taxonomy_terms(self):
        return self.service.taxonomy_terms


def service_to_string(adapter):
    result = f'{adapter.the_id()}, {adapter.name()}, {adapter.description()}'
    taxonomy_terms = {taxonomy_term_to_string(t) for t in adapter.taxonomy_terms()}
    taxonomy_terms = list(taxonomy_terms)
    taxonomy_terms.sort()
    for t in taxonomy_terms:
        result += t
    return result


def taxonomy_term_to_string(taxonomy_term):
    return f'({taxonomy_term.taxonomy_id}:{taxonomy_term.name}) '


def service_already_exists(service):
    return Service.objects.filter(pk=service.id).exists()


def save_service_at_location(service):
    active_record = build_service_at_location_active_record(service)
    active_record.save()
    LOGGER.debug('created service at location: %s %s', service.id, service.site_id)
