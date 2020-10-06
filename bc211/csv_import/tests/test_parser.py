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
        self.assertEqual(parsed_data[0]['organization_id'], the_id)

    def test_can_import_organization_name(self):
        the_name = a_string()
        data = Bc211CsvDataBuilder().with_organization_name(the_name).build()
        parsed_data = parse(data)
        self.assertEqual(parsed_data[0]['organization_name'], the_name)

    def test_can_parse_two_organizations(self):
        first_name = a_string()
        second_name = a_string()
        data = (Bc211CsvDataBuilder().
                with_organization_name(first_name).next_row().
                with_organization_name(second_name).build())
        parsed_data = parse(data)
        self.assertEqual(parsed_data[0]['organization_name'], first_name)
        self.assertEqual(parsed_data[1]['organization_name'], second_name)
