import csv
import os
import logging
from django.utils import translation
from django.core.exceptions import ValidationError
from human_services.organizations.models import Organization
from bc211.import_open_referral_csv import parser
from bc211.import_open_referral_csv.headers_match_expected_format import (
    headers_match_expected_format)
from bc211.import_open_referral_csv.exceptions import InvalidFileCsvImportException

LOGGER = logging.getLogger(__name__)


def import_organizations_file(root_folder, collector, counters):
    filename = 'organizations.csv'
    path = os.path.join(root_folder, filename)
    read_file(path, collector, counters)


def read_file(path, collector, counters):
    with open(path, 'r', newline='') as file:
        reader = csv.reader(file, quoting=csv.QUOTE_ALL, delimiter=',')
        headers = reader.__next__()
        if not headers_match_expected_format(headers, expected_headers):
            raise InvalidFileCsvImportException(
                'The headers in "{0}": does not match open referral standards.'.format(path)
            )
        read_and_import_rows(reader, collector, counters)


expected_headers = ['id', 'name', 'alternate_name', 'description', 'email', 'url',
                'tax_status', 'tax_id', 'year_incorporated', 'legal_status']


def read_and_import_rows(reader, collector, counters):
    for row in reader:
        if not row:
            continue
        import_organization(row, collector, counters)


def import_organization(row, collector, counters):
    try:
        translation.activate('en')
        organization_id = parser.parse_required_field_with_double_escaped_html(
            'organization_id',
            row[0]
        )
        description = parser.parse_optional_field_with_double_escaped_html(row[3])
        if collector.organization_has_inactive_data(organization_id, description):
            return
        active_record = build_active_record(row, organization_id, description)
        active_record.save()
        counters.count_organization_created()
    except ValidationError as error:
        LOGGER.warning('%s', error.__str__())


def build_active_record(row, organization_id, description):
    active_record = Organization()
    active_record.id = organization_id
    active_record.name = parser.parse_required_field_with_double_escaped_html('name', row[1])
    active_record.alternate_name = parser.parse_optional_field_with_double_escaped_html(row[2])
    active_record.description = description
    active_record.email = parser.parse_email(active_record.id, row[4])
    active_record.website = parser.parse_website_with_prefix(active_record.id, row[5])
    return active_record
