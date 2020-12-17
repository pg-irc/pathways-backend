import logging
import csv
from bc211.is_inactive import is_inactive
from bc211.import_xml.parser import parse_agency
from bc211.import_xml.organization import update_entire_organization
from django.contrib.gis.geos import Point
from bc211.import_xml.exceptions import XmlParseException

LOGGER = logging.getLogger(__name__)


def parse_csv(csv_path):
    with open(csv_path, mode='r') as file:
        csv_reader = csv.reader(file)
        city_to_latlong = {rows[0]: Point(float(rows[1]), float(rows[2])) for rows in csv_reader}
        return city_to_latlong


def update_all_organizations(nodes, city_latlong_map, counts):
    last_organization = None
    for _, elem in nodes:
        if elem.tag == 'Agency':
            try:
                agency = parse_agency(elem)
                if is_inactive(agency.description):
                    continue
                last_organization = agency.id
                update_entire_organization(agency, city_latlong_map, counts)
            except XmlParseException as error:
                handle_xml_parser_exception(error, last_organization)
            except AttributeError as error:
                handle_attribute_error(error, last_organization)


def handle_xml_parser_exception(error, last_agency_id):
    LOGGER.error('Parser exception caught when importing the organization immediately after the one with id "%s": "%s"',
                 last_agency_id, error.__str__())


def handle_attribute_error(error, last_agency_id):
    LOGGER.error('Missing field error caught when importing the organization immediately after the one with id "%s": "%s"',
                 last_agency_id, error.__str__())


def handle_parser_errors(generator):
    organization_id = ''
    while True:
        try:
            organization = next(generator)
            organization_id = organization.id
            yield organization
        except StopIteration:
            return
        except XmlParseException as error:
            LOGGER.error('Error importing the organization immediately after the one with id "%s": %s',
                         organization_id, error.__str__())
