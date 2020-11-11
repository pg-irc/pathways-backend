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
                import_service_at_location(row)
    except FileNotFoundError as error:
            LOGGER.error('Missing services_at_location.csv file.')
            raise


def import_service_at_location(row):
    active_record = build_service_at_location_active_record(row)
    active_record.save()
    

def build_service_at_location_active_record(row):
    active_record = ServiceAtLocation()
    active_record.service_id = parser.parse_service_id(row[1])
    active_record.location_id = parser.parse_location_id(row[2])
    return active_record