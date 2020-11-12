import os
import logging
from bc211.open_referral_csv_import import headers_match_expected_format
from bc211.open_referral_csv_import.exceptions import InvalidFileCsvImportException

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
    except FileNotFoundError as error:
            LOGGER.error('Missing phones.csv file.')
            raise


expected_headers = ['id', 'location_id', 'service_id', 'organization_id', 'contact_id', 'service_at_location_id',
                  'number', 'extension', 'type', 'language', 'description', 'department']
