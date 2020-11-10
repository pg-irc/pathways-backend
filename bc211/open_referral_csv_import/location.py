import os
import logging
from .parser import parse_required_field, parse_optional_field, parse_coordinate_if_defined
from bc211.open_referral_csv_import import dtos
from human_services.locations.models import Location
from bc211.is_inactive import is_inactive
from django.contrib.gis.geos import Point

LOGGER = logging.getLogger(__name__)


def import_locations_file(root_folder):
    filename = 'locations.csv'
    path = os.path.join(root_folder, filename)
    try:
        with open(path, 'r') as file: 
            reader = csv.reader(file)
            headers = reader.__next__()
            for row in reader:
                if not row:
                    return
                location = parse_location(row)
                save_location(location)
    except FileNotFoundError as error:
            LOGGER.error('Missing locations.csv file.')
            raise


def parse_location(row):
    location = {}
    location['id'] = parse_required_field('id', row[0])
    location['organization_id'] = parse_required_field('organization_id', row[1])
    location['name'] = parse_required_field('name', row[2])
    location['alternate_name'] = parse_optional_field('alternate_name', row[3])
    location['description'] = parse_optional_field('description', row[4])
    location['latitude'] = parse_coordinate_if_defined('latitude', row[6])
    location['longitude'] = parse_coordinate_if_defined('longitude', row[7])
    return dtos.Location(id=location['id'], organization_id=location['organization_id'], name=location['name'],
                        alternate_name=location['alternate_name'], description=location['description'],
                        spatial_location=dtos.SpatialLocation(latitude=location['latitude'], longitude=location['longitude']))


def save_location(location):
    if is_inactive(location):
        return
    active_record = build_location_active_record(location)
    active_record.save()


def build_location_active_record(location):
    active_record = Location()
    active_record.id = location.id
    active_record.organization_id = location.organization_id
    active_record.name = location.name
    active_record.alternate_name = location.alternate_name
    active_record.description = location.description
    has_location = location.spatial_location is not None
    if has_location:
        active_record.point = Point(location.spatial_location.longitude, location.spatial_location.latitude)
    return active_record