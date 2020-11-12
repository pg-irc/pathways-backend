import os
import logging

LOGGER = logging.getLogger(__name__)


def import_phones_file(root_folder):
    filename = 'phones.csv'
    path = os.path.join(root_folder, filename)
    try:
        with open(path, 'r') as file: 
            reader = csv.reader(file)
            headers = reader.__next__()
    except FileNotFoundError as error:
            LOGGER.error('Missing phones.csv file.')
            raise
