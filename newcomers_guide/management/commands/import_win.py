import os
from django.core.management.base import BaseCommand
from bc211.import_icarol_xml.import_counters import ImportCounters
from newcomers_guide.split_win_file import parse_file

# invoke as follows:
# python manage.py import_win path/to/win/document


class Command(BaseCommand):
    help = 'Import Winnipeg Introduction for Newcomers (WIN) from single text file'

    def add_arguments(self, parser):
        parser.add_argument('file',
                            metavar='file',
                            help='path to the file containing the WIN content')
        parser.add_argument('path',
                            metavar='path',
                            help='path where the output will be written')

    def handle(self, *args, **options):
        inputfile = options['file']
        path = options['path']
        self.stdout.write(f'reading {inputfile}')
        data = parse_file(self.stdout, inputfile)
        self.stdout.write(f'parsed {len(data.topics)} topics')
        for topic in data.topics:
            os.makedirs(topic.file_path(path), exist_ok=True)
            locale = 'en'
            file_name = topic.file_name(path, locale)
            self.stdout.write(f'writing data to {file_name}')
            with open(file_name, 'w') as fp:
                fp.write(topic.text)
