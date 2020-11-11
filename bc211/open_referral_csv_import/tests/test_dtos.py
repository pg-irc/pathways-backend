import unittest
from django.test import TestCase
from ..exceptions import MissingRequiredFieldCsvParseException, InvalidTypeCsvParseException, InvalidFloatCsvParseException
from ..dtos import Address


class AddressDtoTests(TestCase):
    def test_throws_on_missing_type(self):
        with self.assertRaises(MissingRequiredFieldCsvParseException):
            Address(id='id', location_id='location_id', city='city', country='CA')

    def test_throws_on_missing_location_id(self):
        with self.assertRaises(MissingRequiredFieldCsvParseException):
            Address(id='id', type='postal_address', city='city', country='CA')

    def test_throws_on_missing_city(self):
        with self.assertRaises(MissingRequiredFieldCsvParseException):
            Address(id='id', type='postal_address', location_id='location_id', country='CA')

    def test_throws_on_missing_country(self):
        with self.assertRaises(MissingRequiredFieldCsvParseException):
            Address(id='id', type='postal_address', location_id='location_id', city='city')
    
    def tests_throws_on_invalid_type(self):
        with self.assertRaises(InvalidTypeCsvParseException):
            Address(id='id', type='postal_address', location_id='location_id', city='city', country='CA', address=123)
    
    def tests_throws_on_invalid_country_code(self):
        with self.assertRaises(InvalidTypeCsvParseException):
            Address(id='id', type='postal_address', location_id='location_id', city='city', country='CANADA')