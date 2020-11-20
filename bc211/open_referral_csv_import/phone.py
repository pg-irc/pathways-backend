import csv
import os
import logging
from bc211.open_referral_csv_import.headers_match_expected_format import headers_match_expected_format
from bc211.open_referral_csv_import.exceptions import InvalidFileCsvImportException
from human_services.phone_at_location.models import PhoneNumberType, PhoneAtLocation
from bc211.open_referral_csv_import import parser

LOGGER = logging.getLogger(__name__)


def import_phones_file(root_folder):
    filename = 'phones.csv'
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
                import_phone(row)
    except FileNotFoundError as error:
            LOGGER.error('Missing phones.csv file.')
            raise


expected_headers = ['id', 'location_id', 'service_id', 'organization_id', 'contact_id', 'service_at_location_id',
                  'number', 'extension', 'type', 'language', 'description', 'department']


def import_phone(row):
    phone_number_type_active_record = build_phone_number_type_active_record(row)
    phone_number_type_active_record.save()
    phone_at_location_active_record = build_phone_at_location_active_record(row)
    phone_at_location_active_record.save()


def build_phone_number_type_active_record(row):
    active_record = PhoneNumberType()
    active_record.id = parser.parse_required_type(row[8])
    return active_record


def build_phone_at_location_active_record(row):
    active_record = PhoneAtLocation()
    active_record.location_id = parser.parse_location_id(row[1])
    active_record.phone_number = parser.parse_phone_number(row[6])
    phone_type = parser.parse_required_type(row[8])
    active_record.phone_number_type = PhoneNumberType.objects.get(pk=phone_type)
    return active_record