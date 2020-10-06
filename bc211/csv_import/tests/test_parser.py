import logging
from django.test import TestCase
from common.testhelpers.random_test_values import a_string
from ..parser import parse
from .helpers import Bc211CsvDataBuilder

logging.disable(logging.ERROR)


class ParserTests(TestCase):
    def test_can_import_organization_id(self):
        the_id = a_string()
        data = Bc211CsvDataBuilder().with_organization_id(the_id).build()
        parsed_data = parse(data)
        self.assertEqual(parsed_data['organization_id'], the_id)
