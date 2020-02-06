import argparse
from django.core.management.base import BaseCommand
from bc211.importer import parse_csv, update_entire_organization
from bc211.parser import parse_agency
from bc211.import_counters import ImportCounters
from bc211.exceptions import XmlParseException
from human_services.organizations.models import Organization
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
        self.import_from_xml_nodes(nodes, city_latlong_map)

    def import_from_xml_nodes(self, nodes, city_latlong_map):
        counts = ImportCounters()
        agencies = []
        for _, elem in nodes:
            if elem.tag == 'Agency':
                agency_id = self.import_agency(elem, city_latlong_map, counts)
                agencies.append(agency_id)
        self.delete_organizations_not_in(agencies, counts)
        self.print_status_message(counts)

    def import_agency(self, elem, city_latlong_map, counts):
        agency_id = ''
        try:
            agency = parse_agency(elem)
            agency_id = agency.id
            update_entire_organization(agency, city_latlong_map, counts)
            return agency_id

        except XmlParseException as error:
            error = 'Parser exception caught when importing the organization immediately after the one with id "{the_id}": {error_message}'.format(
                the_id=agency_id, error_message=error.__str__())
            self.stdout.write(self.style.ERROR(error))
        except AttributeError as error:
            error = 'Missing field error caught when importing the organization immediately after the one with id "{the_id}": {error_message}'.format(
                the_id=agency_id, error_message=error.__str__())
            self.stdout.write(self.style.ERROR(error))

    def delete_organizations_not_in(self, orgs, counts):
        orgs_to_delete = Organization.objects.exclude(pk__in=orgs).all()
        ids = [o.id for o in orgs_to_delete]
        self.stdout.write(self.style.SUCCESS(f'Orgs to delete: {ids}'))

    def print_status_message(self, counts):
        message = f'{counts.organizations_created} organizations created and {counts.organizations_updated} updated. '
        message += f'{counts.locations_created} locations created and {(counts.locations_updated)} updated. '
        message += f'{counts.service_created} services created and {counts.service_updated} updated. '
        message += f'{counts.taxonomy_term_count} taxonomy terms created. '
        message += f'{counts.address_count} addresses created. '
        message += f'{counts.phone_at_location_count} phone numbers created '
        message += f'and {counts.phone_number_types_count} phone number types created. '

        self.stdout.write(self.style.SUCCESS(message))
