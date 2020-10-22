import argparse
import csv
from django.core.management.base import BaseCommand
from bc211.csv_import.parser import parse
from bc211.csv_import.csv_file_sink import CsvFileSink

# invoke as follows:
# python manage.py import_bc211_csv_data path/to/bc211.csv


class Command(BaseCommand):
    help = 'Convert data in BC211 CSV export format to openReferral standard CSV files'

    def add_arguments(self, parser):
        parser.add_argument('file',
                            type=argparse.FileType('r', encoding='ISO-8859-1'),
                            metavar='file',
                            help='Path to CSV file containing BC-211 data')

    def handle(self, *args, **options):
        parse(CsvFileSink('.'), options['file'])
