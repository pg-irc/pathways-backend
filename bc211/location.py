import logging
from bc211.address import create_address_for_location
from bc211.phone_number import create_phone_numbers_for_location
from bc211.is_inactive import is_inactive
from bc211 import dtos
from django.contrib.gis.geos import Point
from human_services.addresses.models import Address
from human_services.phone_at_location.models import PhoneAtLocation
from human_services.locations.models import Location, LocationAddress
from human_services.locations.models import ServiceAtLocation

LOGGER = logging.getLogger(__name__)


def update_locations(locations, organization_id, city_latlong_map, counters):
    location_ids_to_delete = get_ids_of_locations_to_delete(locations, organization_id)
    delete_locations(location_ids_to_delete)
    for location in locations:
        if is_inactive(location):
            continue
        existing = get_existing_location_or_none(location)
        if not existing:
            save_location(location, None, city_latlong_map, counters)
            counters.count_locations_created()
            LOGGER.info('created "%s" "%s"', location.id, location.name)
        elif not is_location_equal(existing, location):
            save_location(location, existing, city_latlong_map, counters)
            counters.count_locations_updated()
            LOGGER.info('updated "%s" "%s"', location.id, location.name)


def get_ids_of_locations_to_delete(locations, organization_id):
    new_location_ids = [location.id for location in locations if not is_inactive(location)]
    locations_to_delete = (Location.objects.filter(organization_id=organization_id).
                           exclude(pk__in=new_location_ids).
                           all())
    return [location.id for location in locations_to_delete]


def delete_locations(location_ids_to_delete):
    for i in location_ids_to_delete:
        LOGGER.info('delete "%2"', i.id)
    ServiceAtLocation.objects.filter(location_id__in=location_ids_to_delete).delete()
    Location.objects.filter(pk__in=location_ids_to_delete).delete()


def get_existing_location_or_none(location):
    pk = location.id
    if Location.objects.filter(id=pk).exists():
        return Location.objects.get(id=pk)
    return None


def is_location_equal(active_record, dto):
    return hash_from_location_active_record(active_record) == hash_from_location_dto(dto)


def hash_from_location_active_record(location):
    longitude = location.point.x if location.point else None
    latitude = location.point.y if location.point else None
    result = hash_string_from_location(location.id, location.name, location.organization_id,
                                       location.description, longitude, latitude)

    address = LocationAddress.objects.filter(location_id=location.id).filter(address_type_id='physical_address').all()
    if address:
        address = address[0].address
        result += hash_string_from_address(address.address, address.city, address.state_province,
                                           address.postal_code, address.country, 'physical_address')

    address = LocationAddress.objects.filter(location_id=location.id).filter(address_type_id='postal_address').all()
    if address:
        address = address[0].address
        result += hash_string_from_address(address.address, address.city, address.state_province,
                                           address.postal_code, address.country, 'postal_address')

    phone_numbers = PhoneAtLocation.objects.filter(location_id=location.id).all()
    phone_strings = [hash_string_from_phone_number(phone_number.phone_number, phone_number.phone_number_type.id)
                     for phone_number in phone_numbers]
    phone_strings.sort()
    for phone_string in phone_strings:
        result += phone_string

    return result


def hash_from_location_dto(location):
    longitude = location.spatial_location.longitude if location.spatial_location else None
    latitude = location.spatial_location.latitude if location.spatial_location else None
    result = hash_string_from_location(location.id, location.name, location.organization_id,
                                       location.description, longitude, latitude)
    address = location.physical_address
    if address:
        result += hash_string_from_address(address.address_lines, address.city, address.state_province,
                                           address.postal_code, address.country, 'physical_address')
    address = location.postal_address
    if address:
        result += hash_string_from_address(address.address_lines, address.city, address.state_province,
                                           address.postal_code, address.country, 'postal_address')
    phone_strings = [hash_string_from_phone_number(phone_number.phone_number, phone_number.phone_number_type_id)
                     for phone_number in location.phone_numbers]
    phone_strings.sort()
    for phone_string in phone_strings:
        result += phone_string

    return result


def hash_string_from_location(the_id, name, organization_id, description, longitude, latitude):
    return f'{the_id}, {name}, {organization_id}, {description}, {longitude}, {latitude}'


def hash_string_from_address(address, city, state, postal_code, country, the_type):
    return f'{address}, {city}, {state}, {postal_code}, {country}, {the_type}'


def hash_string_from_phone_number(phone_number, the_type):
    return f'{phone_number}, {the_type}'


def save_location(location, existing_active_record, city_latlong_map, counters):
    delete_all_child_records_for_location(location.id)
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


def delete_all_child_records_for_location(location_id):
    address_ids = [i.address_id for i in LocationAddress.objects.filter(location_id=location_id).all()]
    LocationAddress.objects.filter(address_id__in=address_ids).delete()
    Address.objects.filter(id__in=address_ids).delete()
    PhoneAtLocation.objects.filter(location_id=location_id).delete()


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
