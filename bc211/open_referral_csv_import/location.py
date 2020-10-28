import os
import logging
from .parser import parse_required_field, parse_optional_field

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
        else:
            continue
    return location 