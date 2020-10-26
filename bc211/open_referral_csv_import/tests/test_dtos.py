import unittest
from django.test import TestCase
from ..exceptions import MissingRequiredFieldCsvParseException, InvalidTypeCsvParseException
from ..dtos import Organization


class OrganizationDtoTests(TestCase):
    def test_throws_on_missing_id(self):
        with self.assertRaises(MissingRequiredFieldCsvParseException):
            Organization(name='name')

    def test_throws_on_missing_name(self):
        with self.assertRaises(MissingRequiredFieldCsvParseException):
            Organization(id='id')

    def test_throws_on_invalid_type(self):
        with self.assertRaises(InvalidTypeCsvParseException):
            Organization(id='id', name='name', alternate_name=123)