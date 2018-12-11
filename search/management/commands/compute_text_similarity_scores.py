from django.core.management.base import BaseCommand
from newcomers_guide.read_data import read_task_data
from newcomers_guide.parse_data import parse_task_files
from human_services.services.models import Service
from search.compute_similarities import (to_task_ids_and_descriptions,
                                         to_service_ids_and_descriptions,
                                         compute_similarities)
from search.save_tasks import save_tasks
from search.save_similarities import (save_task_similarities,
                                      save_task_service_similarity_scores)


class Command(BaseCommand):
    help = 'Compute text similarity scores between Newcomers\' Guide content and service provider descriptions, store them in the database'

    def add_arguments(self, parser):
        parser.add_argument('newcomers_guide_path',
                            metavar='newcomers_guide_path',
                            help='path to root of Newcomers Guide folder structure')
        parser.add_argument('--related_tasks',
                            dest='related_tasks',
                            type=int,
                            default=10,
                            help='for each task, store this many related tasks')
        parser.add_argument('--related_services',
                            dest='related_services',
                            type=int,
                            default=50,
                            help='for each task, store this many related services')

    def handle(self, *args, **options):
        root_folder = options['newcomers_guide_path']
        related_task_count = options['related_tasks']
        related_service_count = options['related_services']

        print('All task data and task/service similarity data will be deleted and reimported')

        print('Reading tasks...')
        tasks = read_task_descriptions(root_folder)
        task_ids, task_descriptions = to_task_ids_and_descriptions(tasks)
        print('{} tasks read, reading services...'.format(len(task_ids)))
        service_ids, service_descriptions = to_service_ids_and_descriptions(Service.objects.all())

        descriptions = task_descriptions + service_descriptions

        print('{} services read, computing similarities...'.format(len(service_ids)))
        cosine_doc_similarities = compute_similarities(descriptions)

        print('Saving {} tasks...'.format(len(tasks)))
        save_tasks(tasks)
        print('Saving {} task similarities...'.format(len(task_ids)*(len(task_ids)-1)))
        save_task_similarities(task_ids, cosine_doc_similarities, related_task_count)
        print('Saving {} task-service similarities...'.format(len(task_ids)*len(service_ids)))
        save_task_service_similarity_scores(task_ids, service_ids, cosine_doc_similarities, related_service_count)


def read_task_descriptions(root_folder):
    task_data = read_task_data(root_folder)
    return parse_task_files(task_data)
