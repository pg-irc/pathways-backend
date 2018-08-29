from django.core.management.base import BaseCommand
from newcomers_guide.generate_fixtures import (generate_task_fixture, generate_taxonomy_fixture,
                                               generate_article_fixture, set_taxonomy_term_references_on_content,
                                               set_service_query_on_content)
from newcomers_guide.read_data import (read_task_data, read_article_data,
                                       read_taxonomy_data, read_service_query_data)
from newcomers_guide.parse_data import (parse_task_files, parse_article_files,
                                        parse_taxonomy_files, parse_service_query_files)
from newcomers_guide.log_data import log_taxonomies, log_locales


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

        self.stdout.write('Reading Newcomers Guide data from {}'.format(root_folder))

        taxonomy_data = read_taxonomy_data(root_folder)
        taxonomies = parse_taxonomy_files(taxonomy_data)

        service_query_data = read_service_query_data(root_folder)
        service_queries = parse_service_query_files(service_query_data)

        task_data = read_task_data(root_folder)
        tasks = parse_task_files(task_data)
        set_taxonomy_term_references_on_content(taxonomies, tasks['taskMap'])
        set_service_query_on_content(service_queries, tasks['taskMap'])

        article_data = read_article_data(root_folder)
        articles = parse_article_files(article_data)
        set_taxonomy_term_references_on_content(taxonomies, articles)

        log_taxonomies(self.stdout, tasks['taskMap'], articles)
        log_locales(self.stdout, tasks['taskMap'], articles)

        with open('tasks.ts', 'w') as file:
            file.write(generate_task_fixture(tasks))

        with open('articles.ts', 'w') as file:
            file.write(generate_article_fixture(articles))

        with open('taxonomies.ts', 'w') as file:
            file.write(generate_taxonomy_fixture(taxonomies))
