import logging
from bc211.address import create_address_for_location
from bc211.phone_number import create_phone_numbers_for_location
from bc211.is_inactive import is_inactive
from bc211 import dtos
from django.contrib.gis.geos import Point
from human_services.locations.models import Location

LOGGER = logging.getLogger(__name__)


def update_locations(locations, organization_id, city_latlong_map, counters):
    for location in locations:
        if is_inactive(location.description):
            continue
        existing = get_existing_location_or_none(location)
        if not existing:
            save_location(location, None, city_latlong_map, counters)
            counters.count_locations_created()
            LOGGER.debug('created "%s" "%s"', location.id, location.name)
        else:
            LOGGER.warn('duplicate location "%s" "%s"', location.id, location.name)


def get_existing_location_or_none(location):
    pk = location.id
    if Location.objects.filter(id=pk).exists():
        return Location.objects.get(id=pk)
    return None


def save_location(location, existing_active_record, city_latlong_map, counters):
    location = set_latlong_from_address_if_missing(location, city_latlong_map)
    active_record = (existing_active_record if existing_active_record
                     else create_location_active_record_with_id(location.id))
    update_location_properties(location, active_record)
    active_record.save()

    if location.physical_address:
        create_address_for_location(active_record, location.physical_address, counters)
    if location.postal_address:
        create_address_for_location(active_record, location.postal_address, counters)
    if location.phone_numbers:
        create_phone_numbers_for_location(active_record, location.phone_numbers, counters)


def set_latlong_from_address_if_missing(location_dto, city_latlong_map):
    if location_dto.spatial_location is not None:
        return location_dto
    if location_dto.physical_address is None:
        LOGGER.warning('Location with id "%s" does not have LatLong or physical address',
                       location_dto.id)
        return location_dto
    if location_dto.physical_address.city in city_latlong_map:
        replacement_point = city_latlong_map[location_dto.physical_address.city]
        replacement_spatial_location = dtos.SpatialLocation(
            latitude=replacement_point.y,
            longitude=replacement_point.x
        )
        location_dto.spatial_location = replacement_spatial_location
        return location_dto
    LOGGER.warning('Location with id "%s" does not have city to fall back on for LatLong info',
                   location_dto.id)
    return location_dto


def create_location_active_record_with_id(pk):
    record = Location()
    record.id = pk
    return record


def update_location_properties(record, active_record):
    active_record.name = record.name
    active_record.organization_id = record.organization_id
    active_record.description = record.description
    has_location = record.spatial_location is not None
    if has_location:
        active_record.point = Point(record.spatial_location.longitude, record.spatial_location.latitude)
    return active_record
