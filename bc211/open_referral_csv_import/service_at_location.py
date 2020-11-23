import csv
import os
import logging
from bc211.open_referral_csv_import import parser
from human_services.locations.models import ServiceAtLocation
from bc211.open_referral_csv_import.headers_match_expected_format import headers_match_expected_format
from bc211.open_referral_csv_import.exceptions import InvalidFileCsvImportException
from django.core.exceptions import ValidationError

LOGGER = logging.getLogger(__name__)


def import_services_at_location_file(root_folder):
    filename = 'services_at_location.csv'
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
                import_service_at_location(row)
    except FileNotFoundError as error:
            LOGGER.error('Missing services_at_location.csv file.')
            raise


expected_headers = ['id', 'service_id', 'location_id', 'description']


def import_service_at_location(row):
    active_record = build_service_at_location_active_record(row)
    try:
        active_record.save()
    except ValidationError as error:
        LOGGER.warn('{}'.format(error.__str__()))


def build_service_at_location_active_record(row):
    active_record = ServiceAtLocation()
    active_record.service_id = parser.parse_service_id(row[1])
    active_record.location_id = parser.parse_location_id(row[2])
    return active_record