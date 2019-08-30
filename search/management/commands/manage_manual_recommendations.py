import os
from django.core.management.base import BaseCommand
from search.manual_recommendations import read_manual_similarities
from search.models import TaskServiceSimilarityScore

class Command(BaseCommand):
    help = ('')

    def add_arguments(self, parser):
        parser.add_argument('path',
                            metavar='path',
                            help='path to folder containing per-topic files with recommendations')

    def handle(self, *args, **options):
        path = options['path']
        csv_filenames = get_all_csv_filenames_from_folder(path)

        for filename in csv_filenames:
            handle_file(filename)

def handle_file(filename):
    topic_id = get_topic_id_from_filename(filename)
    csv_data = read_manual_similarities(filename)
    handle_data(topic_id, csv_data)

def handle_data(topic_id, csv_data):
    header = csv_data[0]
    service_id_index = get_index_for_header(header, 'service_id')
    exclude_index = get_index_for_header(header, 'Include/Exclude')
    change_records = build_change_records(topic_id, service_id_index, exclude_index, csv_data)
    save_changes_to_database(change_records)

def get_all_csv_filenames_from_folder(path):
    result = []
    directory = os.fsencode(path)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".csv"):
            result.append(filename)
    return result

def get_topic_id_from_filename(path):
    filename = os.path.basename(path)
    return filename.split('.')[0]

def get_index_for_header(row, expected_header):
    for index in range(len(row)):
        if row[index] == expected_header:
            return index
    raise Exception(f'header "{expected_header}" not found')

def build_change_records(topic_id, service_id_index, exclude_index, csv_data):
    make_record = lambda line: {
        'topic_id' : topic_id,
        'service_id' : line[service_id_index],
        'exclude' : line[exclude_index],
    }
    return list(map(make_record, csv_data))

def included_records(change_records):
    return list(filter(lambda record: record['exclude'] != 'Exclude', change_records))

def save_changes_to_database(change_records):
    for record in included_records(change_records):
        save_record(record)


def save_record(record):
    manual_similarity_score = 1.0
    TaskServiceSimilarityScore.objects.update_or_create(
        task_id=record['topic_id'],
        service_id=record['service_id'],
        defaults={
            'similarity_score': manual_similarity_score
        }
    )
