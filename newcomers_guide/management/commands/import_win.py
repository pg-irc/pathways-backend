import os
from django.core.management.base import BaseCommand
from bc211.import_icarol_xml.import_counters import ImportCounters
from newcomers_guide.split_win_file import parse_file

# invoke as follows:
# python manage.py import_win path/to/win/document


class Command(BaseCommand):
    help = 'Import Winnipeg Introduction for Newcomers (WIN) from single text file'

    def add_arguments(self, parser):
        parser.add_argument('path',
                            metavar='path',
                            help='path to the file containing the WIN content')

    def handle(self, *args, **options):
        path = options['path']
        data = parse_file(path)
        for topic in data.topics:
            os.mkdir(topic.file_path())
            file_name = topic.file_name()
            self.stdout.write(f'writing data to {file_name}')
            with open(file_name, 'w') as fp:
                fp.write(topic.text)
