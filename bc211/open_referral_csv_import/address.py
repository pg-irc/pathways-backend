import os
import logging
from .parser import parse_required_field, parse_optional_field
from bc211.open_referral_csv_import import dtos
from human_services.addresses.models import Address, AddressType
from human_services.locations.models import LocationAddress, Location

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
                address_dto = parse_address(headers, row)
                address_active_record = save_address(address_dto)
                save_location_address(address_active_record, address_dto)
    except FileNotFoundError as error:
            LOGGER.error('Missing addresses.csv file.')
            raise


def parse_address(headers, row):
    address = {}
    address['type'] = parse_required_field('type', row[1])
    address['location_id'] = parse_required_field('location_id', row[2])
    address['attention'] = parse_optional_field('attention', row[3])
    address['address'] = parse_optional_field('address', row[4])
    address['city'] = parse_required_field('city', row[8])
    address['state_province'] = parse_optional_field('state_province', row[10])
    address['postal_code'] = parse_optional_field('postal_code', row[11])
    address['country'] = parse_required_field('country', row[12])
    return dtos.Address(type=address['type'], location_id=address['location_id'],
                    attention=address['attention'], address=address['address'], city=address['city'],
                    state_province=address['state_province'], postal_code=address['postal_code'],
                    country=address['country'])


def save_address(address):
    active_record = build_address_active_record(address)
    active_record.save()
    return active_record


def build_address_active_record(address):
    active_record = Address()
    active_record.city = address.city
    active_record.country = address.country
    active_record.attention = address.attention
    active_record.address = address.address
    active_record.state_province = address.state_province
    active_record.postal_code = address.postal_code
    return active_record


def save_location_address(address_active_record, address_dto):
    location = Location.objects.get(pk=address_dto.location_id)
    address_type = AddressType.objects.get(pk=address_dto.type)
    LocationAddress(address=address_active_record, location=location, address_type=address_type).save()