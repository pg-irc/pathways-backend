import argparse
from django.core.management.base import BaseCommand
from bc211.import_xml.importer import parse_csv, update_all_organizations
from bc211.import_xml.import_counters import ImportCounters
import xml.etree.ElementTree as etree

# invoke as follows:
# python manage.py import_xml path/to/bc211.xml


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
        counts = ImportCounters()
        nodes = etree.iterparse(file, events=('end',))
        update_all_organizations(nodes, city_latlong_map, counts)
        self.print_status_message(counts)

    def print_status_message(self, counts):
        message = f'{counts.organizations_created} organizations created. '
        message += f'{counts.locations_created} locations created. '
        message += f'{counts.services_created} services created. '
        message += f'{counts.taxonomy_term_count} taxonomy terms created. '
        message += f'{counts.address_count} addresses created. '
        message += f'{counts.phone_at_location_count} phone numbers created '
        message += f'and {counts.phone_number_types_count} phone number types created. '

        self.stdout.write(self.style.SUCCESS(message))
