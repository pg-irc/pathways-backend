import unittest
from django.test import TestCase
from ..exceptions import MissingRequiredFieldCsvParseException, InvalidTypeCsvParseException, InvalidFloatCsvParseException
from ..dtos import Organization, Service, Location, SpatialLocation, ServiceAtLocation, Address


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
    def test_throws_on_missing_id(self):
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


class LocationDtoTests(TestCase):
    def test_throws_on_missing_id(self):
        with self.assertRaises(MissingRequiredFieldCsvParseException):
            Location(organization_id='organization_id')
    
    def test_throws_on_missing_organization_id(self):
        with self.assertRaises(MissingRequiredFieldCsvParseException):
            Location(id='id')
    
    def tests_throws_on_missing_name(self):
        with self.assertRaises(MissingRequiredFieldCsvParseException):
            Location(id='id', organization_id='organization_id')
    
    def tests_throws_on_invalid_type(self):
        with self.assertRaises(InvalidTypeCsvParseException):
            Location(id='id', organization_id='organization_id', name='name', alternate_name=123)

    def tests_throws_on_invalid_spatial_location_type(self):
        with self.assertRaises(InvalidFloatCsvParseException):
            Location(id='id', organization_id='organization_id', name='name', spatial_location=SpatialLocation(latitude='foo', longitude='-23.456'))


class ServiceAtLocationDtoTests(TestCase):
    def test_throws_on_missing_service_id(self):
        with self.assertRaises(MissingRequiredFieldCsvParseException):
            ServiceAtLocation(location_id='location_id')

    def test_throws_on_missing_location_id(self):
        with self.assertRaises(MissingRequiredFieldCsvParseException):
            ServiceAtLocation(service_id='service_id')


class AddressDtoTests(TestCase):
    def test_throws_on_missing_address_id(self):
        with self.assertRaises(MissingRequiredFieldCsvParseException):
            Address(type='postal_address', location_id='location_id', city='city', country='CA')
    
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