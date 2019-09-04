from django.core.management.base import BaseCommand
from search.read_similarities import build_manual_similarity_map
from search.save_similarities import save_manual_similarities
from search.read_manual_similarities import read_manual_similarities


class Command(BaseCommand):
    help = ('Set text similarity scores from CSV file between Newcomers\' Guide '
            'content and service provider descriptions, store them in the database')

    def add_arguments(self, parser):
        parser.add_argument('manual_similarities',
                            metavar='manual_similarities',
                            help='path to file containing manual similarities from topics to services')

    def handle(self, *args, **options):
        manual_similarities_path = options['manual_similarities']

        manual_similarities_csv = read_manual_similarities(manual_similarities_path)
        manual_similarities_map = build_manual_similarity_map(manual_similarities_csv)
        print('Saving manual topic-service similarities...')
        save_manual_similarities(manual_similarities_map)
