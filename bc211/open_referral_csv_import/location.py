import os
import logging
from .parser import parse_required_field

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
    for header in headers:
        if header == 'id':
            location['id'] = parse_required_field('id', location_id)
        else:
            continue
    return location 
