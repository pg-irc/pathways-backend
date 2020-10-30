import os
import logging
from .parser import parse_required_field

LOGGER = logging.getLogger(__name__)


def import_services_at_location_file(root_folder):
    filename = 'services_at_location.csv'
    path = os.path.join(root_folder, filename)
    try:
        with open(path, 'r') as file: 
            reader = csv.reader(file)
            headers = reader.__next__()
            for row in reader:
                if not row:
                    return
                service_at_location = parse_service_at_location(headers, row)
    except FileNotFoundError as error:
            LOGGER.error('Missing services_at_location.csv file.')
            raise


def parse_service_at_location(headers, row):
    service_at_location = {}
    service_id = row[1]
    location_id = row[2]
    for header in headers:
        if header == 'service_id':
            service_at_location['service_id'] = parse_required_field('service_id', service_id)
        elif header == 'location_id':
            service_at_location['location_id'] = parse_required_field('location_id', location_id)
        else: 
            continue
    return service_at_location