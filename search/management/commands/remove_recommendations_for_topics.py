from django.core.management.base import BaseCommand
from search.read_similarities import (read_manual_similarities,
                                      build_manual_similarity_map,
                                      save_manual_similarities)
from search.remove_similarities_for_topics import remove_similarities_for_topics


class Command(BaseCommand):
    help = ('For topics for which there are no meaningful services to recommend, '
            'remove all recommended services')

    def add_arguments(self, parser):
        parser.add_argument('topics_list',
                            metavar='topics_list',
                            help=('path to file containing list of ids of topics to remove, '
                                  'one topic per line'))

    def handle(self, *args, **options):
        topics_list_path = options['topics_list']

        topics_ids = read_manual_similarities(topics_list_path)
        print('Saving manual task-service similarities...')
        remove_similarities_for_topics(topics_ids)
