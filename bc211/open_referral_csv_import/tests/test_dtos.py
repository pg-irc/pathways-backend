import unittest
from django.test import TestCase
from ..exceptions import MissingRequiredFieldCsvParseException, InvalidTypeCsvParseException
from ..dtos import Organization, Service


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


class ServiceDtoTests(TestCase):
    def tests_throws_on_missing_id(self):
        with self.assertRaises(MissingRequiredFieldCsvParseException):
            Service(organization_id='organization_id')
    
    def test_throws_on_missing_organization_id(self):
        with self.assertRaises(MissingRequiredFieldCsvParseException):
            Service(id='id')
    
    def tests_throws_on_missing_name(self):
        with self.assertRaises(MissingRequiredFieldCsvParseException):
            Service(id='id', organization_id='organization_id')
    
    def tests_throws_on_invalid_type(self):
        with self.assertRaises(InvalidTypeCsvParseException):
            Service(id='id', organization_id='organization_id', name='name', alternate_name=123)