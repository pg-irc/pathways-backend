import os
import logging
from .parser import parse_required_field, parse_optional_field

LOGGER = logging.getLogger(__name__)


def import_addresses_file(root_folder):
    filename = 'addresses.csv'
    path = os.path.join(root_folder, filename)
    try:
        with open(path, 'r') as file: 
            reader = csv.reader(file)
            headers = reader.__next__()
            for row in reader:
                if not row:
                    return
                address = parse_address(headers, row)
    except FileNotFoundError as error:
            LOGGER.error('Missing addresses.csv file.')
            raise


def parse_address(headers, row):
    address = {}
    address_id = row[0]
    address_type = row[1]
    location_id = row[2]
    attention = row[3]
    address_address = row[4]
    city = row[8]
    state_province = row[10]
    postal_code = row[11]
    for header in headers:
        if header == 'id':
            address['id'] = parse_required_field('id', address_id)
        if header == 'type':
            address['type'] = parse_required_field('type', address_type)
        elif header == 'location_id':
            address['location_id'] = parse_required_field('location_id', location_id)
        elif header == 'attention':
            address['attention'] = parse_optional_field('attention', attention)
        elif header == 'address_1':
            address['address'] = parse_optional_field('address', address_address)
        elif header == 'city':
            address['city'] = parse_required_field('city', city)
        elif header == 'state_province':
            address['state_province'] = parse_optional_field('state_province', state_province)
        elif header == 'postal_code':
            address['postal_code'] = parse_optional_field('postal_code', postal_code)
        else:
            continue
    return address