import os
import logging
from human_services.addresses.models import Address, AddressType
from human_services.locations.models import LocationAddress, Location
from bc211.open_referral_csv_import import parser

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
                import_address_and_location_address(row)
    except FileNotFoundError as error:
            LOGGER.error('Missing addresses.csv file.')
            raise


def import_address_and_location_address(row):
    address_active_record = build_address_active_record(row)
    address_active_record.save()
    location_address_active_record = build_location_address_active_record(address_active_record, row)
    location_address_active_record.save()


def save_address(address):
    active_record = build_address_active_record(address)
    active_record.save()
    return active_record


def build_address_active_record(row):
    active_record = Address()
    active_record.city = parser.parse_city(row[8])
    active_record.country = parser.parse_country(row[12])
    active_record.attention = parser.parse_attention(row[3])
    active_record.address = parser.parse_address(row[4])
    active_record.state_province = parser.parse_state_province(row[10])
    active_record.postal_code = parser.parse_postal_code(row[11])
    return active_record


def build_location_address_active_record(address_active_record, row):
    address_type = parser.parse_required_type(row[1])
    location_id = parser.parse_location_id(row[2])
    location_instance = Location.objects.get(pk=location_id)
    address_type_instance = AddressType.objects.get(pk=address_type)
    return LocationAddress(address=address_active_record, location=location_instance, address_type=address_type_instance)