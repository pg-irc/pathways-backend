import logging
from human_services.addresses.models import Address, AddressType
from human_services.locations.models import LocationAddress

LOGGER = logging.getLogger(__name__)


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
    LOGGER.debug(f'created location address {address}')
    return active_record
