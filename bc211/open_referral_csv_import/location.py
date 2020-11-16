import csv
import os
import logging
from bc211.open_referral_csv_import import parser
from human_services.locations.models import Location
from bc211.is_inactive import is_inactive
from django.contrib.gis.geos import Point
from bc211.open_referral_csv_import import headers_match_expected_format
from bc211.open_referral_csv_import.exceptions import InvalidFileCsvImportException

LOGGER = logging.getLogger(__name__)


def import_locations_file(root_folder):
    filename = 'locations.csv'
    path = os.path.join(root_folder, filename)
    try:
        with open(path, 'r') as file: 
            reader = csv.reader(file)
            headers = reader.__next__()
            if not headers_match_expected_format(headers, expected_headers):
                raise InvalidFileCsvImportException('The headers in "{0}": does not match open referral standards.'.format(field))
            for row in reader:
                if not row:
                    return
                import_location(row)
    except FileNotFoundError as error:
            LOGGER.error('Missing locations.csv file.')
            raise


expected_headers = ['id', 'organization_id', 'name', 'alternate_name', 'description',
                'transportation', 'latitude', 'longitude']


def import_location(row):
    active_record = build_location_active_record(row)
    if is_inactive(active_record):
        return
    active_record.save()


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