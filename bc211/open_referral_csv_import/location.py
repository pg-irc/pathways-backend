import os
import logging
from .parser import parse_required_field, parse_optional_field, parse_coordinate_if_defined
from bc211.open_referral_csv_import import dtos
from human_services.locations.models import Location
from bc211.is_inactive import is_inactive

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
                location = parse_location(headers, row)
                save_location(location)
    except FileNotFoundError as error:
            LOGGER.error('Missing locations.csv file.')
            raise


def parse_location(headers, row):
    location = {}
    location_id = row[0]
    organization_id = row[1]
    name = row[2]
    alternate_name = row[3]
    description = row[4]
    latitude = row[6]
    longitude = row[7]
    for header in headers:
        if header == 'id':
            location['id'] = parse_required_field('id', location_id)
        elif header == 'organization_id':
            location['organization_id'] = parse_required_field('organization_id', organization_id)
        elif header == 'name':
            location['name'] = parse_required_field('name', name)
        elif header == 'alternate_name':
            location['alternate_name'] = parse_optional_field('alternate_name', alternate_name)
        elif header == 'description':
            location['description'] = parse_optional_field('description', description)
        elif header == 'latitude':
            location['latitude'] = parse_coordinate_if_defined('latitude', latitude)
        elif header == 'longitude':
            location['longitude'] = parse_coordinate_if_defined('longitude', longitude)
        else:
            continue
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
    return active_record