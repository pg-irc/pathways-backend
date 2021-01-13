import csv
import os
import logging
from django.core.exceptions import ValidationError
from bc211.import_open_referral_csv import parser
from bc211.import_open_referral_csv.headers_match_expected_format import (
    headers_match_expected_format)
from bc211.import_open_referral_csv.exceptions import InvalidFileCsvImportException
from human_services.services.models import Service

LOGGER = logging.getLogger(__name__)


def import_services_file(root_folder, collector, counters):
    filename = 'services.csv'
    path = os.path.join(root_folder, filename)
    read_file(path, collector, counters)


def read_file(path, collector, counters):
    with open(path, 'r', newline='') as file:
        reader = csv.reader(file)
        headers = reader.__next__()
        if not headers_match_expected_format(headers, expected_headers):
            raise InvalidFileCsvImportException(
                'The headers in "{0}": does not match open referral standards.'.format(path)
            )
        read_and_import_rows(reader, collector, counters)



expected_headers = ['id', 'organization_id', 'program_id', 'name', 'alternate_name',
                'description', 'url', 'email', 'status', 'interpretation_services',
                'application_process', 'wait_time', 'fees', 'accreditations',
                'licenses', 'taxonomy_ids', 'last_verified_on-x']


def read_and_import_rows(reader, collector, counters):
    for row in reader:
        if not row:
            continue
        import_service(row, collector, counters)


def import_service(row, collector, counters):
    try:
        service_id = parser.parse_required_field_with_double_escaped_html('service_id', row[0])
        organization_id = parser.parse_required_field_with_double_escaped_html(
            'organization_id',
            row[1]
        )
        description = parser.parse_optional_field_with_double_escaped_html(row[5])
        if collector.service_has_inactive_data(organization_id, service_id, description):
            return
        active_record = build_service_active_record(row, service_id, organization_id, description)
        active_record.save()
        counters.count_service()
    except ValidationError as error:
        LOGGER.warning('%s', error.__str__())


def build_service_active_record(row, service_id, organization_id, description):
    active_record = Service()
    active_record.id = service_id
    active_record.organization_id = organization_id
    active_record.name = parser.parse_required_field_with_double_escaped_html('name', row[3])
    active_record.alternate_name = parser.parse_optional_field_with_double_escaped_html(row[4])
    active_record.description = description
    active_record.website = parser.parse_website_with_prefix(active_record.id, row[6])
    active_record.email = parser.parse_email(active_record.id, row[7])
    active_record.last_verified_date = parser.parse_last_verified_date(row[16])
    return active_record
