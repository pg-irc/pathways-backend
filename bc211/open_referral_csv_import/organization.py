import os
import logging
from bc211.open_referral_csv_import import dtos
from django.utils import translation
from human_services.organizations.models import Organization
from bc211.open_referral_csv_import import parser
from bc211.is_inactive import is_inactive

LOGGER = logging.getLogger(__name__)


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
                organization = parse_organization(row)
                save_organization(organization)
    except FileNotFoundError as error:
            LOGGER.error('Missing organizations.csv file.')
            raise


def parse_organization(row):
    organization = {}
    organization['id'] = parser.parse_organization_id(row[0])
    organization['name'] = parser.parse_required_field('name', row[1])
    organization['alternate_name'] = parser.parse_optional_field('alternate_name', row[2])
    organization['description'] = parser.parse_optional_field('description', row[3])
    organization['email'] = parser.parse_optional_field('email', row[4])
    organization['website'] = parser.parse_website_with_prefix('website', row[5])
    return organization


def save_organization(organization):
    # if is_inactive(organization):
    #     return
    translation.activate('en')
    active_record = build_active_record(organization)
    active_record.save()


def build_active_record(organization):
    active_record = Organization()
    active_record.id = organization['id']
    active_record.name = organization['name']
    active_record.alternate_name = organization['alternate_name']
    active_record.description = organization['description']
    active_record.email = organization['email']
    active_record.website = organization['website']
    return active_record
