import csv
import os
import logging
from django.core.exceptions import ValidationError
from bc211.open_referral_csv_import import parser
from bc211.open_referral_csv_import.headers_match_expected_format import (
    headers_match_expected_format)
from bc211.open_referral_csv_import.exceptions import InvalidFileCsvImportException
from bc211.open_referral_csv_import.inactive_foreign_key import (
    has_inactive_service_id, has_inactive_location_id)
from human_services.locations.models import ServiceAtLocation

LOGGER = logging.getLogger(__name__)


def import_services_at_location_file(root_folder, collector, counters):
    filename = 'services_at_location.csv'
    path = os.path.join(root_folder, filename)
    read_file(path, collector, counters)


def read_file(path, collector, counters):
    with open(path, 'r') as file:
        reader = csv.reader(file)
        headers = reader.__next__()
        if not headers_match_expected_format(headers, expected_headers):
            raise InvalidFileCsvImportException(
                'The headers in "{0}": does not match open referral standards.'.format(path)
            )
        read_and_import_rows(reader, collector, counters)


expected_headers = ['id', 'service_id', 'location_id', 'description']


def read_and_import_rows(reader, collector, counters):
    for row in reader:
        if not row or service_at_location_has_invalid_data(row, collector):
            continue
        import_service_at_location(row, counters)


def service_at_location_has_invalid_data(row, collector):
    service_id = parser.parse_service_id(row[1])
    location_id = parser.parse_location_id(row[2])
    return (has_inactive_service_id(service_id, collector) or
            has_inactive_location_id(location_id, collector))


def import_service_at_location(row, counters):
    try:
        active_record = build_service_at_location_active_record(row)
        active_record.save()
        counters.count_service_at_location()
    except ValidationError as error:
        LOGGER.warning('%s', error.__str__())


def build_service_at_location_active_record(row):
    active_record = ServiceAtLocation()
    active_record.service_id = parser.parse_service_id(row[1])
    active_record.location_id = parser.parse_location_id(row[2])
    return active_record
