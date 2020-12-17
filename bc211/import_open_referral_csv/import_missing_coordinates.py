import logging
from human_services.locations.models import LocationAddress

LOGGER = logging.getLogger(__name__)


def import_missing_coordinates(city_latlong_map):
    records_without_latlong = (
        LocationAddress.objects.filter(location__point__isnull=True, address__city__isnull=False)
    )
    for active_record in records_without_latlong:
        set_latlong_from_city(active_record, city_latlong_map)


def set_latlong_from_city(active_record, city_latlong_map):
    if active_record.address.city in city_latlong_map:
        replacement_point = city_latlong_map[active_record.address.city]
        active_record.location.point = replacement_point
        active_record.location.save()
    else:
        LOGGER.warning('City "%s" does not have a latlong associated with it.',
                        active_record.address.city)
