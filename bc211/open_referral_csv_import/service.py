import csv
import os
import logging
from bc211.open_referral_csv_import import parser
from human_services.services.models import Service
from bc211.open_referral_csv_import.is_inactive import is_inactive
from bc211.open_referral_csv_import.headers_match_expected_format import headers_match_expected_format
from bc211.open_referral_csv_import.exceptions import InvalidFileCsvImportException

LOGGER = logging.getLogger(__name__)


def import_services_file(root_folder):
    filename = 'services.csv'
    path = os.path.join(root_folder, filename)
    try:
        with open(path, 'r') as file: 
            reader = csv.reader(file)
            headers = reader.__next__()
            if not headers_match_expected_format(headers, expected_headers):
                raise InvalidFileCsvImportException('The headers in "{0}": does not match open referral standards.'.format(field))
            for row in reader:
                if not row:
                    return
                import_service(row)
    except FileNotFoundError as error:
            LOGGER.error('Missing services.csv file.')
            raise


expected_headers = ['id', 'organization_id', 'program_id', 'name', 'alternate_name', 'description',
                'url', 'email', 'status', 'interpretation_services', 'application_process',
                'wait_time', 'fees', 'accreditations', 'licenses', 'taxonomy_ids', 'last_verified_on-x']


def import_service(row):
    description = parser.parse_description(row[5])
    if is_inactive(description):
        return
    active_record = build_service_active_record(row)
    active_record.save()


def build_service_active_record(row):
    active_record = Service()
    active_record.id = parser.parse_service_id(row[0])
    active_record.organization_id = parser.parse_organization_id(row[1])
    active_record.name = parser.parse_name(row[3])
    active_record.alternate_name = parser.parse_alternate_name(row[4])
    active_record.description = parser.parse_description(row[5])
    active_record.website = parser.parse_website_with_prefix(row[6])
    active_record.email = parser.parse_email(row[7])
    active_record.last_verified_date = parser.parse_last_verified_date(row[16])
    return active_record