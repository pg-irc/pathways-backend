import logging
from django.contrib.gis.geos import Point
from human_services.locations.models import Location, ServiceAtLocation, LocationAddress

LOGGER = logging.getLogger(__name__)


def import_missing_coordinates(city_latlong_map):
    location_addresses_with_city_and_missing_point = (
        LocationAddress.objects.filter(location__point__isnull=True, address__city__isnull=False)
    )
    for active_record in location_addresses_with_city_and_missing_point:
        set_latlong_from_city(active_record, city_latlong_map)


def set_latlong_from_city(active_record, city_latlong_map):
    if active_record.address.city in city_latlong_map:
        replacement_point = city_latlong_map[active_record.address.city]
        active_record.location.point = replacement_point
        active_record.location.save()
    else:
        LOGGER.warn(f'City "{active_record.address.city}" does not have a latlong associated with it.')