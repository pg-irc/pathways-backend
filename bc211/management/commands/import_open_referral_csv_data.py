import argparse
from django.core.management.base import BaseCommand
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

    def handle(self, *args, **options):
        root_folder = options['path']
        self.stdout.write('Importing open referral CSV data from {}'.format(root_folder))
        collector = InactiveRecordsCollector()
        import_open_referral_files(root_folder, collector)
