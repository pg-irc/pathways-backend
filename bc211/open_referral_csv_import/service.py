import os
import logging
from .parser import parse_required_field

LOGGER = logging.getLogger(__name__)


def import_services_file(root_folder):
    filename = 'services.csv'
    path = os.path.join(root_folder, filename)
    try:
        with open(path, 'r') as file: 
            reader = csv.reader(file)
            headers = reader.__next__()
            for row in reader:
                if not row:
                    return
                service = parse_service(headers, row)
    except FileNotFoundError as error:
            LOGGER.error('Missing services.csv file.')
            raise


def parse_service(headers, row):
    service = {}
    service_id = row[0]
    organization_id = row[1]
    name = row[3]
    for header in headers:
        if header == 'id':
            service['id'] = parse_required_field('id', service_id)
        elif header == 'organization_id':
            service['organization_id'] = parse_required_field('organization_id', organization_id)
        elif header == 'name':
            service['name'] = parse_required_field('name', name)
        else:
            continue
    return service