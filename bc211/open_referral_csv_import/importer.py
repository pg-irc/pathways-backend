import os
import logging
from bc211.parser import remove_double_escaped_html_markup

LOGGER = logging.getLogger(__name__)


def import_open_referral_files(root_folder):
    try:
        import_organizations_file(root_folder)
    except Exception as error:
        LOGGER.error(error)

    
def import_organizations_file(root_folder):
    filename = 'organizations.csv'
    path = os.path.join(root_folder, filename)
    try:
        with open(path, 'r') as file: 
            reader = csv.reader(file)
            headers = reader.__next__()
            for row in reader:
                if not row:
                    return
                organization = parse_organization(headers, row)
    except FileNotFoundError as error:
            LOGGER.error('Missing organizations.csv file.')
            raise


def parse_organization(headers, row):
    organization = {}
    organization_id = row[0]
    for header in headers:
        if header == 'id':
            organization['id'] = parse_required_field('id', organization_id)
        else:
            continue
    return organization


def parse_required_field(field, value):
    try:
        return remove_double_escaped_html_markup(value)
    except AttributeError:
        LOGGER.error('Missing required field: "{0}"'.format(field))
        raise