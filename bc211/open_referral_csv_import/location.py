import csv
import os
import logging
from bc211.open_referral_csv_import import parser
from human_services.locations.models import Location
from bc211.is_inactive import is_inactive
from django.contrib.gis.geos import Point
from bc211.open_referral_csv_import.headers_match_expected_format import headers_match_expected_format
from bc211.open_referral_csv_import.exceptions import InvalidFileCsvImportException
from bc211.open_referral_csv_import.inactive_foreign_key import has_inactive_organization_id
from django.core.exceptions import ValidationError

LOGGER = logging.getLogger(__name__)


def import_locations_file(root_folder, collector, counters):
    filename = 'location.csv'
    path = os.path.join(root_folder, filename)
    with open(path, 'r') as file: 
        reader = csv.reader(file)
        headers = reader.__next__()
        if not headers_match_expected_format(headers, expected_headers):
            raise InvalidFileCsvImportException('The headers in "{0}": does not match open referral standards.'.format(field))
        for row in reader:
            if not row or location_has_inactive_data(row, collector):
                continue
            import_location(row, counters)


expected_headers = ['id', 'organization_id', 'name', 'alternate_name', 'description',
                'transportation', 'latitude', 'longitude']


def location_has_inactive_data(row, collector):
    location_id = parser.parse_location_id(row[0])
    organization_id = parser.parse_organization_id(row[1])
    description = parser.parse_description(row[4])

    if is_inactive(description):
        collector.add_inactive_location_id(location_id)
        return True
    if has_inactive_organization_id(organization_id, collector):
        return True
    return False


def import_location(row, counters):
    try:
        active_record = build_location_active_record(row)
        active_record.save()
        counters.count_locations_created()
    except ValidationError as error:
        LOGGER.warn('{}'.format(error.__str__()))

def build_location_active_record(row):
    active_record = Location()
    active_record.id = parser.parse_location_id(row[0])
    active_record.organization_id = parser.parse_organization_id(row[1])
    active_record.name = parser.parse_name(row[2])
    active_record.alternate_name = parser.parse_alternate_name(row[3])
    active_record.description = parser.parse_description(row[4])
    latitude = parser.parse_coordinate_if_defined(row[6])
    longitude = parser.parse_coordinate_if_defined(row[7])
    if not has_coordinates(latitude, longitude):
        LOGGER.warning('Location with id "%s" does not have LatLong defined', active_record.id)
    active_record.point = Point(longitude, latitude)
    return active_record


def has_coordinates(latitude, longitude):
    return latitude and longitude is not None