import os
import logging
from bc211.open_referral_csv_import import parser
from human_services.locations.models import ServiceAtLocation

LOGGER = logging.getLogger(__name__)


def import_services_at_location_file(root_folder):
    filename = 'services_at_location.csv'
    path = os.path.join(root_folder, filename)
    try:
        with open(path, 'r') as file: 
            reader = csv.reader(file)
            headers = reader.__next__()
            for row in reader:
                if not row:
                    return
                service_at_location = parse_service_at_location(row)
                save_service_at_location(service_at_location)
    except FileNotFoundError as error:
            LOGGER.error('Missing services_at_location.csv file.')
            raise


def parse_service_at_location(row):
    service_at_location = {}
    service_at_location['service_id'] = parser.parse_service_id(row[1])
    service_at_location['location_id'] = parser.parse_location_id(row[2])
    return service_at_location


def save_service_at_location(service_at_location):
    active_record = build_service_at_location(service_at_location)
    active_record.save()

def build_service_at_location(service_at_location):
    active_record = ServiceAtLocation()
    active_record.service_id = service_at_location['service_id']
    active_record.location_id = service_at_location['location_id']
    return active_record