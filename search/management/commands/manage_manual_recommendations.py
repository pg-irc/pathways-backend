import os
from django.core.management.base import BaseCommand
from search.manual_recommendations import read_manual_similarities

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
            topic_id = get_topic_id_from_filename(filename)
            csv_data = read_manual_similarities(filename)
            header = csv_data[0]
            service_id_index = get_index_for_header(header, 'service_id')
            exclude_index = get_index_for_header(header, 'Include/Exclude')
            change_records = build_change_records(topic_id, service_id_index, exclude_index, csv_data)

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
    raise Exception("header ${expected_header} not found")

def build_change_records(topic_id, service_id_index, exclude_index, csv_data):
    result = []
    for line in csv_data:
        result.append({
            'topic_id' : topic_id,
            'service_id' : line[service_id_index],
            'exclude' : line[exclude_index],
        })
    return result
