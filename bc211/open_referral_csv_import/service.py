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
                service = parse_service(row)
                save_service(service)
    except FileNotFoundError as error:
            LOGGER.error('Missing services.csv file.')
            raise


def parse_service(row):
    service = {}
    service['id'] = parser.parse_service_id(row[0])
    service['organization_id'] = parser.parse_organization_id(row[1])
    service['name'] = parser.parse_name(row[3])
    service['alternate_name'] = parser.parse_alternate_name(row[4])
    service['description'] = parser.parse_description(row[5])
    service['website'] = parser.parse_website_with_prefix('website', row[6])
    service['email'] = parser.parse_email(row[7])
    return service


def save_service(service):
    # if is_inactive(service):
    #     return
    active_record = build_service_active_record(service)
    active_record.save()
    

def build_service_active_record(service):
    active_record = Service()
    active_record.id = service['id']
    active_record.organization_id = service['organization_id']
    active_record.name = service['name']
    active_record.alternate_name = service['alternate_name']
    active_record.description = service['description']
    active_record.website = service['website']
    active_record.email = service['email']
    return active_record