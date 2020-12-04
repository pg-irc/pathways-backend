import argparse
from django.core.management.base import BaseCommand
from bc211.importer import parse_csv
from bc211.import_counters import ImportCounters
from bc211.open_referral_csv_import.importer import import_open_referral_files
from bc211.open_referral_csv_import.inactive_records_collector import InactiveRecordsCollector

# invoke as follows:
# python manage.py import_open_referral_csv_data path/to/open/referral/files


class Command(BaseCommand):
    help = 'Import BC211 data from open referral standard CSV files'

    def add_arguments(self, parser):
        parser.add_argument('path',
                            metavar='path',
                            help='Path to directory containing open referral CSV BC-211 data')
        parser.add_argument('--cityLatLongs',
                            metavar='cityLatLongs',
                            help='Path to CSV file containing city to latlong dictionary')

    def handle(self, *args, **options):
        root_folder = options['path']

        if options['cityLatLongs']:
            city_latlong_map = parse_csv(options['cityLatLongs'])
        else:
            city_latlong_map = {}

        self.stdout.write('Importing open referral CSV data from {}'.format(root_folder))
        collector = InactiveRecordsCollector()
        counters = ImportCounters()
        import_open_referral_files(root_folder, collector, counters, city_latlong_map)
        self.print_status_message(counters)

    def print_status_message(self, counters):
        message = f'{counters.organizations_created} organizations created. '
        message += f'{counters.locations_created} locations created. '
        message += f'{counters.services_created} services created. '
        message += f'{counters.service_at_location_count} services_at_location created. '
        message += f'{counters.taxonomy_term_count} taxonomy terms created. '
        message += f'{counters.address_count} addresses created. '
        message += f'{counters.location_address_count} location addresses created. '
        message += f'{counters.phone_at_location_count} phone numbers created '
        message += f'and {counters.phone_number_types_count} phone number types created. '

        self.stdout.write(self.style.SUCCESS(message))
