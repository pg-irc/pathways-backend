import csv
import os
import logging
from bc211.open_referral_csv_import.headers_match_expected_format import headers_match_expected_format
from bc211.open_referral_csv_import.exceptions import InvalidFileCsvImportException
from bc211.open_referral_csv_import import parser
from human_services.services.models import Service
from taxonomies.models import TaxonomyTerm

LOGGER = logging.getLogger(__name__)


def import_services_taxonomy_file(root_folder):
    filename = 'services_taxonomy.csv'
    path = os.path.join(root_folder, filename)
    try:
        with open(path, 'r') as file: 
            reader = csv.reader(file)
            headers = reader.__next__()
            if not headers_match_expected_format(headers, expected_headers):
                raise InvalidFileCsvImportException('The headers in "{0}": does not match open referral standards.'.format(field))
    except FileNotFoundError as error:
            LOGGER.error('Missing services_taxonomy.csv file.')
            raise


expected_headers = ['id', 'service_id', 'taxonomy_id', 'taxonomy_detail']


def import_service_taxonomy(row):
    service_id = parser.parse_service_id(row[1])
    taxonomy_id = parser.parse_taxonomy_id(row[2])
    save_service_taxonomy_term(service_id, taxonomy_id)


def save_service_taxonomy_term(service_id, taxonomy_id):
    service_active_record = Service.objects.get(id=service_id)
    taxonomy_term = TaxonomyTerm.objects.get(taxonomy_id=taxonomy_id)
    service_active_record.taxonomy_terms.add(taxonomy_term)
    service_active_record.save()