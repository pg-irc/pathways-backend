import os
import logging
from bc211.open_referral_csv_import import dtos
from django.utils import translation
from human_services.organizations.models import Organization
from .parser import parse_required_field, parse_optional_field, parse_website_with_prefix

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
                organization = parse_organization(headers, row)
                save_organization(organization)
    except FileNotFoundError as error:
            LOGGER.error('Missing organizations.csv file.')
            raise


def save_organization(organization):
    translation.activate('en')
    active_record = build_active_record(organization)
    active_record.save()


def build_active_record(organization):
    active_record = Organization()
    active_record.id = organization.id
    active_record.name = organization.name
    active_record.alternate_name = organization.alternate_name
    active_record.description = organization.description
    active_record.email = organization.email
    active_record.website = organization.website
    return active_record


def parse_organization(headers, row):
    organization = {}
    organization_id = row[0]
    name = row[1]
    alternate_name = row[2]
    description = row[3]
    email = row[4]
    website = row[5]
    for header in headers:
        if header == 'id':
            organization['id'] = parse_required_field('id', organization_id)
        elif header == 'name':
            organization['name'] = parse_required_field('name', name)
        elif header == 'alternate_name':
            organization['alternate_name'] = parse_optional_field('alternate_name', alternate_name)
        elif header == 'description':
            organization['description'] = parse_optional_field('description', description)
        elif header == 'email':
            organization['email'] = parse_optional_field('email', email)
        elif header == 'url':
            organization['website'] = parse_website_with_prefix('website', website)
        else:
            continue
    return dtos.Organization(id=organization['id'], name=organization['name'], alternate_name=organization['alternate_name'],
                        description=organization['description'], website=organization['website'], email=organization['email'])