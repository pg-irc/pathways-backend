import csv
import os
import logging
from django.utils import translation
from human_services.organizations.models import Organization
from bc211.is_inactive import is_inactive
from bc211.open_referral_csv_import import parser
from bc211.open_referral_csv_import.headers_match_expected_format import headers_match_expected_format
from bc211.open_referral_csv_import.exceptions import InvalidFileCsvImportException

LOGGER = logging.getLogger(__name__)


def import_organizations_file(root_folder, collector):
    filename = 'organizations.csv'
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
                import_organization(row, collector)
    except FileNotFoundError as error:
            LOGGER.error('Missing organizations.csv file.')
            raise


expected_headers = ['id', 'name', 'alternate_name', 'description', 'email', 'url',
                'tax_status', 'tax_id', 'year_incorporated', 'legal_status']


def import_organization(row, collector):
    translation.activate('en')
    organization_id = parser.parse_organization_id(row[0])
    description = parser.parse_description(row[3])
    if is_inactive(description):
        collector.add_inactive_organization_id(organization_id)
        return
    active_record = build_active_record(row)
    active_record.save()


def build_active_record(row):
    active_record = Organization()
    active_record.id = parser.parse_organization_id(row[0])
    active_record.name = parser.parse_name(row[1])
    active_record.alternate_name = parser.parse_alternate_name(row[2])
    active_record.description = parser.parse_description(row[3])
    active_record.email = parser.parse_email(active_record.id, row[4])
    active_record.website = parser.parse_website_with_prefix(active_record.id, row[5])
    return active_record
