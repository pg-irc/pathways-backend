import os
import logging

LOGGER = logging.getLogger(__name__)


def import_open_referral_files(root_folder):
    try:
        parse_organization_file(root_folder)
    except Exception as error:
        LOGGER.error(error)

    
def import_organizations_file(root_folder):
    filename = 'organizations.csv'
    path = os.path.join(root_folder, filename)
    try:
        with open(path, 'r') as file: 
            reader = csv.reader(file)
    except FileNotFoundError as error:
            LOGGER.error('Missing organizations.csv file.')
            raise