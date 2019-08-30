import csv
from io import StringIO
from django.test import TestCase
from human_services.organizations.tests.helpers import OrganizationBuilder
from human_services.services.tests.helpers import ServiceBuilder
from common.testhelpers.random_test_values import a_string
from newcomers_guide.tests.helpers import create_topic
from search.models import TaskServiceSimilarityScore
from search.management.commands.manage_manual_recommendations import get_index_for_header, build_change_records, get_topic_id_from_filename

# example https://docs.google.com/spreadsheets/d/1CSNCvpNwqX8VnxGESbcKOo_nlhcINZHXhrmCPyyvBXQ/edit?ts=5d696373#gid=471688895

class TestReadManualRecommendationsFile(TestCase):

    def test_get_index_of_column(self):
        result = get_index_for_header(['topic_id', 'score', 'service_id', 'exclude?'], 'service_id')
        self.assertEqual(result, 2)

    def test_throw_on_missing_header(self):
        with self.assertRaises(Exception):
            get_index_for_header(['invalid_topic_id', 'score', 'service_id', 'exclude?'], 'topic_id')

    def test_get_topic_id_from_filename(self):
        result = get_topic_id_from_filename('path/to/topic_id.csv')
        self.assertEqual(result, 'topic_id')

    def test_get_topic_id_from_filename_with_no_extension(self):
        result = get_topic_id_from_filename('path/to/topic_id')
        self.assertEqual(result, 'topic_id')

class TestBuildChangeRecords(TestCase):
    def setUp(self):
        self.topic_id = a_string()
        self.service_id = a_string()

    def test_reads_topic_id_from_argument(self):
        service_id_index = 0
        exclude_index = 1
        csv_data = [self.service_id, 'Include']

        result = build_change_records(self.topic_id, service_id_index, exclude_index, csv_data)

        self.assertEqual(result['topic_id'], self.topic_id)

    def test_reads_service_id_from_column_with_given_index(self):
        service_id_index = 3
        exclude_index = 4
        csv_data = [0, 0, 0, self.service_id, 'Include']

        result = build_change_records(self.topic_id, service_id_index, exclude_index, csv_data)

        self.assertEqual(result['service_id'], self.service_id)

    def test_reads_exclude_flag_from_column_with_given_index(self):
        service_id_index = 3
        exclude_index = 4
        csv_data = [0, 0, 0, self.service_id, 'Include']

        result = build_change_records(self.topic_id, service_id_index, exclude_index, csv_data)

        self.assertEqual(result['exclude'], 'Include')
