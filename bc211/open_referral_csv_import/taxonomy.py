import csv
import os
import logging
from bc211.open_referral_csv_import.headers_match_expected_format import headers_match_expected_format
from bc211.open_referral_csv_import.exceptions import InvalidFileCsvImportException
from bc211.open_referral_csv_import import parser
from taxonomies.models import TaxonomyTerm

LOGGER = logging.getLogger(__name__)


def import_taxonomy_file(root_folder):
    filename = 'taxonomy.csv'
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
                import_taxonomy(row)
    except FileNotFoundError as error:
            LOGGER.error('Missing taxonomy.csv file.')
            raise


expected_headers = ['id', 'name', 'parent_id', 'parent_name', 'vocabulary']


def import_taxonomy(row):
    active_record = build_taxonomy_active_record(row)
    active_record.save()


def build_taxonomy_active_record(row):
    active_record = TaxonomyTerm()
    active_record.taxonomy_id = parser.parse_taxonomy_id(row[0])
    active_record.name = parser.parse_name(row[1])
    return active_record
    