import csv
from io import StringIO
from django.test import TestCase

def validate_column_headers(headers):
    if headers[0] != 'topic_id':
        raise Exception("'topic_id' expected in the first column")

    if headers[1] != 'score':
        raise Exception("'score' expected in the second column")

    if headers[2] != 'service_id':
        raise Exception("'service_id' expected in the third column")

    if headers[3] != 'exclude?':
        raise Exception("'exclude?' expected in the fourth column")

class TestReadManualRecommendationsFile(TestCase):

    def foo(self):
        # data = 'topic_id,score,service_id,exclude?'
        # reader = csv.reader(StringIO(data), delimiter=',')
        # row = next(reader, None)
        # self.assertEqual(row, ['topic_id', 'score', 'service_id', 'exclude?'])

    def test_validates_column_headers(self):
        validate_column_headers(['topic_id', 'score', 'service_id', 'exclude?'])

        with self.assertRaises(Exception):
            validate_column_headers(['invalid_topic_id', 'score', 'service_id', 'exclude?'])

        with self.assertRaises(Exception):
            validate_column_headers(['topic_id', 'invalid_score', 'service_id', 'exclude?'])

        with self.assertRaises(Exception):
            validate_column_headers(['topic_id', 'score', 'invalid_service_id', 'exclude?'])

        with self.assertRaises(Exception):
            validate_column_headers(['topic_id', 'score', 'service_id', 'invalid_exclude?'])

    def test_bla(self):
        data = 'foo,bar,baz\n1,2,3'
        reader = csv.reader(StringIO(data), delimiter=',')
        row = next(reader, None)
        self.assertEqual(row, ['foo', 'bar', 'baz'])
