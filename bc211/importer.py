import logging
import csv
from bc211 import dtos
from django.utils import translation
from django.contrib.gis.geos import Point
from human_services.locations.models import Location, ServiceAtLocation, LocationAddress
from human_services.organizations.models import Organization
from human_services.services.models import Service
from human_services.addresses.models import Address, AddressType
from human_services.phone_at_location.models import PhoneNumberType, PhoneAtLocation
from taxonomies.models import TaxonomyTerm
from bc211.exceptions import XmlParseException
from search.models import TaskServiceSimilarityScore

LOGGER = logging.getLogger(__name__)


def parse_csv(csv_path):
    with open(csv_path, mode='r') as file:
        csv_reader = csv.reader(file)
        city_to_latlong = {rows[0]: Point(float(rows[1]), float(rows[2])) for rows in csv_reader}
        return city_to_latlong


def update_entire_organization(organization, city_latlong_map, counters):
    update_organization(organization, counters)
    locations = list(organization.locations)
    update_locations(locations, organization.id, city_latlong_map, counters)
    for location in locations:
        if not is_inactive(location):
            update_services_for_location(location.id, location.services, counters)


def update_organization(organization, counters):
    if is_inactive(organization):
        return
    translation.activate('en')
    existing = get_existing_organization_or_none(organization)
    if not existing:
        active_record = build_organization_active_record(organization)
        active_record.save()
        counters.count_organization_created()
        LOGGER.debug('Organization "%s" "%s"', organization.id, organization.name)
    elif not is_organization_equal(existing, organization):
        active_record = build_organization_active_record(organization)
        active_record.save()
        counters.count_organizations_updated()
        LOGGER.debug('Organization "%s" "%s"', organization.id, organization.name)


def get_existing_organization_or_none(organization):
    result = Organization.objects.filter(id=organization.id).all()
    return result[0] if result else None


def is_organization_equal(active_record, dto):
    return (hash_string_for_organization(active_record) == hash_string_for_organization(dto))


def hash_string_for_organization(org):
    return f'{org.id}, {org.name}, {org.description}, {org.website}, {org.email}'


def handle_parser_errors(generator):
    organization_id = ''
    while True:
        try:
            organization = next(generator)
            organization_id = organization.id
            yield organization
        except StopIteration:
            return
        except XmlParseException as error:
            LOGGER.error('Error importing the organization immediately after the one with id "%s": %s',
                         organization_id, error.__str__())


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
        elif not is_location_equal(existing, location):
            save_location(location, existing, city_latlong_map, counters)
            counters.count_locations_updated()


def get_ids_of_locations_to_delete(locations, organization_id):
    new_location_ids = [location.id for location in locations if not is_inactive(location)]
    locations_to_delete = (Location.objects.filter(organization_id=organization_id).
                           exclude(pk__in=new_location_ids).
                           all())
    return [location.id for location in locations_to_delete]


def delete_locations(location_ids_to_delete):
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
    LOGGER.debug('Location "%s" "%s"', location.id, location.name)

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


def is_inactive(record):
    # This is BC211's convention for marking records as inactive
    return record.description and record.description.strip().startswith('DEL')


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


def build_service_active_record(record):
    active_record = get_or_create_service_active_record(record.id)
    active_record.name = record.name
    active_record.organization_id = record.organization_id
    active_record.description = record.description
    active_record.last_verified_date = record.last_verified_date
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
    new_service_ids = [s.id for s in services if not is_inactive(s)]
    links_to_delete = ServiceAtLocation.objects.filter(location_id=location_id).exclude(service_id__in=new_service_ids).all()
    services_to_delete = [s.service_id for s in links_to_delete]
    ServiceAtLocation.objects.filter(pk__in=[s.id for s in links_to_delete]).delete()
    TaskServiceSimilarityScore.objects.filter(service_id__in=services_to_delete).delete()
    Service.objects.filter(pk__in=services_to_delete).delete()
    for service in services:
        save_service_if_needed(service, counters)


def save_service_if_needed(service, counters):
    delete_existing_service_taxonomy_terms(service)
    if is_inactive(service):
        return
    existing = get_existing_service_or_none(service)
    if not existing:
        active_record = build_service_active_record(service)
        active_record.save()
        counters.count_service()
        LOGGER.debug('Service "%s" "%s"', service.id, service.name)
        save_service_at_location(service)
        save_service_taxonomy_terms(service.taxonomy_terms, active_record, counters)
    elif not is_service_equal(existing, service):
        active_record = build_service_active_record(service)
        active_record.save()
        counters.count_services_updates()
        LOGGER.debug('Service "%s" "%s"', service.id, service.name)
        save_service_at_location(service)
        save_service_taxonomy_terms(service.taxonomy_terms, active_record, counters)


def get_existing_service_or_none(service):
    pk = service.id
    if Service.objects.filter(id=pk).exists():
        return Service.objects.get(id=pk)
    return None


def is_service_equal(active_record, dto):
    return service_to_string(ArAdaptor(active_record)) == service_to_string(DtoAdapter(dto))


class ArAdaptor:
    def __init__(self, service):
        self.service = service

    def the_id(self):
        return self.service.id

    def name(self):
        return self.service.name

    def description(self):
        return self.service.description


class DtoAdapter:
    def __init__(self, service):
        self.service = service

    def the_id(self):
        return self.service.id

    def name(self):
        return self.service.name

    def description(self):
        return self.service.description


def service_to_string(adapter):
    return f'{adapter.the_id()}, {adapter.name()}, {adapter.description()}'


def delete_existing_service_taxonomy_terms(service):
    for s in Service.objects.filter(pk=service.id):
        s.taxonomy_terms.clear()


def service_already_exists(service):
    return Service.objects.filter(pk=service.id).exists()


def save_service_at_location(service):
    active_record = build_service_at_location_active_record(service)
    active_record.save()
    LOGGER.debug('Service at location: %s %s', service.id, service.site_id)


def save_service_taxonomy_terms(taxonomy_terms, service_active_record, counters):
    for taxonomy_term in taxonomy_terms:
        taxonomy_term_active_record = create_taxonomy_term_active_record(
            taxonomy_term,
            counters
        )
        service_active_record.taxonomy_terms.add(taxonomy_term_active_record)
        LOGGER.debug('Imported service taxonomy term')
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
    delete_existing_location_address(location, address_type)
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
        LOGGER.debug('Address: %s %s', active_record.id, active_record.address)
    return active_record


def delete_existing_location_address(location, address_type):
    location_addresses = LocationAddress.objects.filter(location_id=location.id).filter(address_type=address_type).all()
    for location_address in location_addresses:
        address_id = location_address.address.id
        location_address.delete()
        Address.objects.filter(pk=address_id).delete()


def create_location_address(location, address, address_type):
    active_record = LocationAddress(address=address, location=location,
                                    address_type=address_type).save()
    LOGGER.debug('Location address')
    return active_record


def create_phone_numbers_for_location(location, phone_number_dtos, counters):
    PhoneAtLocation.objects.filter(location_id=location.id).delete()
    for dto in phone_number_dtos:
        phone_number_type = create_phone_number_type(dto, counters)
        number = PhoneAtLocation.objects.create(
            location=location,
            phone_number_type=phone_number_type,
            phone_number=dto.phone_number
        )
        counters.count_phone_at_location()
        LOGGER.debug('PhoneNumber: "%s" "%s"', number.id, number.phone_number)


def create_phone_number_type(dto, counters):
    type_id = dto.phone_number_type_id
    phone_number_type, created = PhoneNumberType.objects.get_or_create(id=type_id)
    if created:
        counters.count_phone_number_types()
        LOGGER.debug('PhoneNumberType: "%s"', phone_number_type.id)
    return phone_number_type
