import argparse
from django.core.management.base import BaseCommand
from bc211.importer import parse_csv, save_locations, save_organization, save_services
from bc211.parser import parse_agency
from bc211.import_counters import ImportCounters
from bc211.exceptions import XmlParseException
import xml.etree.ElementTree as etree

# invoke as follows:
# python manage.py import_bc211_data path/to/bc211.xml


class Command(BaseCommand):
    help = 'Import BC-211 data from XML file'

    def add_arguments(self, parser):
        parser.add_argument('file',
                            type=argparse.FileType('r'),
                            metavar='file',
                            help='Path to XML file containing BC-211 data')
        parser.add_argument('--cityLatLongs',
                            metavar='cityLatLongs',
                            help='Path to CSV file containing city to latlong dictionary')

    def handle(self, *args, **options):
        file = options['file']
        if options['cityLatLongs']:
            city_latlong_map = parse_csv(options['cityLatLongs'])
        else:
            city_latlong_map = {}
        nodes = etree.iterparse(file, events=('end',))
        self.parse_agencies(nodes, city_latlong_map)

    def parse_agencies(self, nodes, city_latlong_map):
        counts = ImportCounters()
        organization_id = ''
        for _, elem in nodes:
            if elem.tag == 'Agency':
                try:
                    organization = parse_agency(elem)
                    organization_id = organization.id

                    save_organization(organization, counts)
                    save_locations(organization.locations, city_latlong_map, counts)

                except XmlParseException as error:
                    error = 'Parser exception caught when importing the organization immediately after the one with id "{the_id}": {error_message}'.format(
                        the_id=organization_id, error_message=error.__str__())
                    self.stdout.write(self.style.ERROR(error))
                except AttributeError as error:
                    error = 'Missing field error caught when importing the organization immediately after the one with id "{the_id}": {error_message}'.format(
                        the_id=organization_id, error_message=error.__str__())
                    self.stdout.write(self.style.ERROR(error))
        self.print_status_message(counts)

    def print_status_message(self, counts):
        message_template = ('Successfully imported {0} organization(s), '
                            '{1} location(s), {2} service(s), '
                            '{3} taxonomy term(s), {4} address(es), {5} phone number type(s), '
                            'and {6} phone number(s)')
        status_message = message_template.format(counts.organization_count,
                                                 counts.location_count,
                                                 counts.service_count,
                                                 counts.taxonomy_term_count,
                                                 counts.address_count,
                                                 counts.phone_number_types_count,
                                                 counts.phone_at_location_count)
        self.stdout.write(self.style.SUCCESS(status_message))
