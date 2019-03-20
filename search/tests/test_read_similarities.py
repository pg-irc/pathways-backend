from django.test import TestCase
from search.read_similarities import build_manual_similarity_map
from common.testhelpers.random_test_values import a_string, a_float


class TestReadingManualTaskSimilarities(TestCase):
    def test_deletes_existing_records(self):
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
