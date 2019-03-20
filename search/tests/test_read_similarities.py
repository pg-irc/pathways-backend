from django.test import TestCase
from search.read_similarities import build_manual_similarity_map
from common.testhelpers.random_test_values import a_string, a_float


class TestReadingManualTaskSimilarities(TestCase):
    def test_convert_matrix_to_map_from_topic_to_array_of_services(self):
        data = [
            ['topic1', 'topic2'],
            ['service1', 'service2'],
        ]
        expected_result = {
            'topic1': ['service1'],
            'topic2': ['service2'],
        }
        result = build_manual_similarity_map(data)
        self.assertEqual(result, expected_result)

    def test_can_handle_multiple_services_for_a_topic(self):
        data = [
            ['topic1', ],
            ['service1'],
            ['service2'],
            ['service3'],
        ]
        expected_result = {
            'topic1': ['service1', 'service2', 'service3'],
        }
        result = build_manual_similarity_map(data)
        self.assertEqual(result, expected_result)

    def test_can_handle_different_numbers_of_services_for_different_topics(self):
        data = [
            ['topic1', 'topic2'],
            ['service1', 'service2'],
            ['service3'],
        ]
        expected_result = {
            'topic1': ['service1', 'service3'],
            'topic2': ['service2'],
        }
        result = build_manual_similarity_map(data)
        self.assertEqual(result, expected_result)

    def test_can_handle_empty_entries(self):
        data = [
            ['topic1', 'topic2'],
            ['service1', 'service2'],
            ['', 'service3'],  # TODO need to confirm what the CSV library does here
            [None, 'service4'],  # TODO need to confirm what the CSV library does here
        ]
        expected_result = {
            'topic1': ['service1'],
            'topic2': ['service2', 'service3', 'service4'],
        }
        result = build_manual_similarity_map(data)
        self.assertEqual(result, expected_result)
