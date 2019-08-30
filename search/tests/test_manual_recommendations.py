from django.test import TestCase
from human_services.organizations.tests.helpers import OrganizationBuilder
from human_services.services.tests.helpers import ServiceBuilder
from common.testhelpers.random_test_values import a_string
from newcomers_guide.tests.helpers import create_topic
from search.models import TaskServiceSimilarityScore
from search.management.commands.manage_manual_recommendations import get_index_for_header, build_change_records, get_topic_id_from_filename, save_changes_to_database

# example https://docs.google.com/spreadsheets/d/1CSNCvpNwqX8VnxGESbcKOo_nlhcINZHXhrmCPyyvBXQ/edit?ts=5d696373#gid=471688895

class TestReadManualRecommendationsFile(TestCase):

    def test_get_index_of_column(self):
        result = get_index_for_header(['topic_id', 'score', 'service_id', 'exclude?'], 'service_id')
        self.assertEqual(result, 2)

    def test_throw_on_missing_header(self):
        with self.assertRaisesRegex(Exception, r'header "topic_id" not found'):
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
        csv_data = [[self.service_id, 'Include']]

        result = build_change_records(self.topic_id, service_id_index, exclude_index, csv_data)

        self.assertEqual(result[0]['topic_id'], self.topic_id)

    def test_reads_service_id_from_column_with_given_index(self):
        service_id_index = 3
        exclude_index = 4
        csv_data = [[0, 0, 0, self.service_id, 'Include']]

        result = build_change_records(self.topic_id, service_id_index, exclude_index, csv_data)

        self.assertEqual(result[0]['service_id'], self.service_id)

    def test_reads_exclude_flag_from_column_with_given_index(self):
        service_id_index = 3
        exclude_index = 4
        csv_data = [[0, 0, 0, self.service_id, 'Include']]

        result = build_change_records(self.topic_id, service_id_index, exclude_index, csv_data)

        self.assertEqual(result[0]['exclude'], 'Include')

    def test_reads_multiple_lines(self):
        service_id_index = 0
        exclude_index = 1
        first_service = a_string()
        second_service = a_string()
        csv_data = [
            [first_service, a_string()],
            [second_service, a_string()],
        ]

        result = build_change_records(self.topic_id, service_id_index, exclude_index, csv_data)

        self.assertEqual(result[0]['service_id'], first_service)
        self.assertEqual(result[1]['service_id'], second_service)

class TestSaveChangesToDatabase(TestCase):
    def setUp(self):
        self.organization = OrganizationBuilder().create()
        self.service = ServiceBuilder(self.organization).create()

    def test_saves_a_record(self):
        topic_id = a_string()
        create_topic(topic_id)

        save_changes_to_database([{'topic_id':topic_id, 'service_id':self.service.id, 'exclude':''}])

        records = TaskServiceSimilarityScore.objects.order_by('similarity_score')
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].task_id, topic_id)
        self.assertEqual(records[0].service_id, self.service.id)
        self.assertAlmostEqual(records[0].similarity_score, 1.0)

    def test_saves_multiple_records(self):
        topic_id = a_string()
        create_topic(topic_id)

        second_topic_id = a_string()
        create_topic(second_topic_id)

        save_changes_to_database([
            {'topic_id':topic_id, 'service_id':self.service.id, 'exclude':''},
            {'topic_id':second_topic_id, 'service_id':self.service.id, 'exclude':''},
        ])

        records = TaskServiceSimilarityScore.objects.order_by('similarity_score')
        self.assertEqual(len(records), 2)

    def test_does_not_save_records_marked_with_exclude(self):
        topic_id = a_string()
        create_topic(topic_id)

        save_changes_to_database([{'topic_id':topic_id, 'service_id':self.service.id, 'exclude':'Exclude'}])

        records = TaskServiceSimilarityScore.objects.order_by('similarity_score')
        self.assertEqual(len(records), 0)

    def test_saves_records_marked_include(self):
        topic_id = a_string()
        create_topic(topic_id)

        save_changes_to_database([{'topic_id':topic_id, 'service_id':self.service.id, 'exclude':'Include'}])

        records = TaskServiceSimilarityScore.objects.order_by('similarity_score')
        self.assertEqual(len(records), 1)

    def test_saves_records_marked_with_arbitrary_string(self):
        topic_id = a_string()
        create_topic(topic_id)

        save_changes_to_database([{'topic_id':topic_id, 'service_id':self.service.id, 'exclude':a_string()}])

        records = TaskServiceSimilarityScore.objects.order_by('similarity_score')
        self.assertEqual(len(records), 1)

