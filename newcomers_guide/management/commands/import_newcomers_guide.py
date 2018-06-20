import os
from django.core.management.base import BaseCommand

# invoke as follows:
# python manage.py import_newcomers_guide path/to/newcomers/root/directory


class Command(BaseCommand):
    help = 'Import Newcomers Guide from folder structure'

    def add_arguments(self, parser):
        parser.add_argument('path',
                            metavar='path',
                            help='path to root of Newcomers Guide folder structure')

    def handle(self, *args, **options):
        root_folder = options['path']

        self.stdout.write(self.style.SUCCESS('Reading Newcomers Guide data from {}'.format(root_folder)))

        for root, _, files in os.walk(root_folder, topdown=False):
            for name in files:
                print(os.path.join(root, name))
