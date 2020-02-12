import logging
from human_services.phone_at_location.models import PhoneNumberType, PhoneAtLocation

LOGGER = logging.getLogger(__name__)


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
        LOGGER.debug('created phone number: "%s" "%s"', number.id, number.phone_number)


def create_phone_number_type(dto, counters):
    type_id = dto.phone_number_type_id
    phone_number_type, created = PhoneNumberType.objects.get_or_create(id=type_id)
    if created:
        counters.count_phone_number_types()
        LOGGER.debug('created phone number type: "%s"', phone_number_type.id)
    return phone_number_type
