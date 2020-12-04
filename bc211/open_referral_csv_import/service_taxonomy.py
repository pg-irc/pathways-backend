import csv
import os
import logging
from bc211.open_referral_csv_import.headers_match_expected_format import headers_match_expected_format
from bc211.open_referral_csv_import.exceptions import InvalidFileCsvImportException
from bc211.open_referral_csv_import import parser
from human_services.services.models import Service
from bc211.open_referral_csv_import.inactive_foreign_key import has_inactive_service_id
from taxonomies.models import TaxonomyTerm
from django.core.exceptions import ObjectDoesNotExist, ValidationError

LOGGER = logging.getLogger(__name__)


def import_services_taxonomy_file(root_folder, collector):
    filename = 'services_taxonomy.csv'
    path = os.path.join(root_folder, filename)
    read_file(path, collector)
    

def read_file(path, collector):
    with open(path, 'r') as file: 
        reader = csv.reader(file)
        headers = reader.__next__()
        if not headers_match_expected_format(headers, expected_headers):
            raise InvalidFileCsvImportException('The headers in "{0}": does not match open referral standards.'.format(field))
        read_and_import_rows(reader, collector)


expected_headers = ['id', 'service_id', 'taxonomy_id', 'taxonomy_detail']


def read_and_import_rows(reader, collector):
    last_service_active_record = None
    last_service_taxonomy_list = []

    for row in reader:
        service_id = parser.parse_service_id(row[1])
        if not row or has_inactive_service_id(service_id, collector):
            continue
        import_service_taxonomy(row, last_service_active_record, last_service_taxonomy_list)


def import_service_taxonomy(row, last_service_active_record, last_service_taxonomy_list):
    try:
        last_service_id = last_service_active_record.id if last_service_active_record else None
        current_service_id = parser.parse_service_id(row[1])
        taxonomy_id = parser.parse_taxonomy_id(row[2])
        taxonomy_term = get_taxonomy_term_active_record_or_raise(taxonomy_id)
        current_active_record = None

        if current_service_id is last_service_id:
            last_service_active_record.taxonomy_term.add(taxonomy_term)
            last_service_taxonomy_list.append(last_service_active_record)
        else:
            if last_service_taxonomy_list:
                Service.objects.bulk_update(last_service_taxonomy_list)
            last_service_taxonomy_list.clear()
            current_active_record = build_service_taxonomy_active_record(current_service_id, taxonomy_term)
            last_service_active_record = current_active_record 
    except ValidationError as error:
        LOGGER.warn('{}'.format(error.__str__()))
    except ObjectDoesNotExist as error:
        pass
        
        
def build_service_taxonomy_active_record(service_id, taxonomy_term):
    service_active_record = get_service_active_record_or_raise(service_id)
    service_active_record.taxonomy_terms.add(taxonomy_term)
    return service_active_record


def get_service_active_record_or_raise(service_id):
    try:
        return Service.objects.get(pk=service_id)
    except ObjectDoesNotExist as error:
        LOGGER.warn('Service record with id "{}" does not exist. {}'.format(service_id, error))
        raise


def get_taxonomy_term_active_record_or_raise(taxonomy_id):
    try:
        return TaxonomyTerm.objects.get(taxonomy_id=taxonomy_id)
    except ObjectDoesNotExist as error:
        LOGGER.warn('Taxonomy record with id "{}" does not exist. {}'.format(service_id, error))
        raise