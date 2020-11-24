import csv
import os
import logging
from human_services.addresses.models import Address, AddressType
from human_services.locations.models import LocationAddress, Location
from bc211.open_referral_csv_import import parser
from bc211.open_referral_csv_import.headers_match_expected_format import headers_match_expected_format
from bc211.open_referral_csv_import.exceptions import InvalidFileCsvImportException
from django.core.exceptions import ObjectDoesNotExist

LOGGER = logging.getLogger(__name__)


def import_addresses_file(root_folder):
    filename = 'addresses.csv'
    path = os.path.join(root_folder, filename)
    try:
        with open(path, 'r') as file: 
            reader = csv.reader(file)
            headers = reader.__next__()
            if not headers_match_expected_format(headers, expected_headers):
                raise InvalidFileCsvImportException('The headers in "{0}": does not match open referral standards.'.format(field))
            for row in reader:
                if not row:
                    continue
                import_address_and_location_address(row)
    except FileNotFoundError as error:
            LOGGER.error('Missing addresses.csv file.')
            raise


expected_headers = ['id', 'type', 'location_id', 'attention', 'address_1', 'address_2', 'address_3',
                'address_4', 'city', 'region', 'state_province', 'postal_code', 'country']


def import_address_and_location_address(row):
    address_active_record = build_address_active_record(row)
    address_active_record.save()
    location_address_active_record = build_location_address_active_record(address_active_record, row)
    if location_address_active_record:
        location_address_active_record.save()


def build_address_active_record(row):
    active_record = Address()
    active_record.id = parser.parse_address_id(row[0])
    active_record.attention = parser.parse_attention(row[3])
    addresses = [row[4], row[5], row[6], row[7]]
    active_record.address = parser.parse_addresses(addresses)
    active_record.city = parser.parse_city(row[8])
    active_record.state_province = parser.parse_state_province(row[10])
    active_record.postal_code = parser.parse_postal_code(row[11])
    active_record.country = parser.parse_country(row[12])
    return active_record


def build_location_address_active_record(address_active_record, row):
    address_type = parser.parse_required_type(row[1])
    location_id = parser.parse_location_id(row[2])
    try:
        location_active_record = get_active_record_or_none(location_id, Location)
        address_type_active_record = get_active_record_or_none(address_type, AddressType)
    except ObjectDoesNotExist as error:
        return
    return LocationAddress(address=address_active_record, location=location_active_record, address_type=address_type_active_record)


def get_active_record_or_none(active_record_id, model):
    try:
        return model.objects.get(pk=active_record_id)
    except ObjectDoesNotExist as error:
        LOGGER.warn('Record with id {} does not exist. {}'.format(active_record_id, error))
        raise