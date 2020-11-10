import os
import logging
from bc211.open_referral_csv_import import parser
from bc211.open_referral_csv_import import dtos
from human_services.services.models import Service
from bc211.is_inactive import is_inactive

LOGGER = logging.getLogger(__name__)


def import_services_file(root_folder):
    filename = 'services.csv'
    path = os.path.join(root_folder, filename)
    try:
        with open(path, 'r') as file: 
            reader = csv.reader(file)
            headers = reader.__next__()
            for row in reader:
                if not row:
                    return
                import_service(row)
    except FileNotFoundError as error:
            LOGGER.error('Missing services.csv file.')
            raise


def import_service(row):
    active_record = build_service_active_record(row)
    if is_inactive(active_record):
        return
    active_record.save()
    

def build_service_active_record(row):
    active_record = Service()
    active_record.id = parser.parse_service_id(row[0])
    active_record.organization_id = parser.parse_organization_id(row[1])
    active_record.name = parser.parse_name(row[3])
    active_record.alternate_name = parser.parse_alternate_name(row[4])
    active_record.description = parser.parse_description(row[5])
    active_record.website = parser.parse_website_with_prefix('website', row[6])
    active_record.email = parser.parse_email(row[7])
    return active_record