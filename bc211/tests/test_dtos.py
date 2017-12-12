import unittest
from bc211 import dtos, exceptions

class TestOrganization(unittest.TestCase):
    def test_throws_on_missing_id(self):
        with self.assertRaises(exceptions.MissingRequiredFieldXmlParseException):
            dtos.Organization(name='name')

    def test_throws_on_missing_name(self):
        with self.assertRaises(exceptions.MissingRequiredFieldXmlParseException):
            dtos.Organization(id='id')

class TestLocation(unittest.TestCase):
    def test_throws_on_missing_id(self):
        with self.assertRaises(exceptions.MissingRequiredFieldXmlParseException):
            dtos.Location(name='name', organization_id='organization_id')

    def test_throws_on_missing_name(self):
        with self.assertRaises(exceptions.MissingRequiredFieldXmlParseException):
            dtos.Location(id='id', organization_id='organization_id')

    def test_throws_on_missing_organization_id(self):
        with self.assertRaises(exceptions.MissingRequiredFieldXmlParseException):
            dtos.Location(id='id', name='name')


class TestSpatialLocation(unittest.TestCase):
    def test_can_create(self):
        location = dtos.SpatialLocation(latitude='123.456', longitude='-23.456')
        self.assertAlmostEqual(location.latitude, 123.456)
        self.assertAlmostEqual(location.longitude, -23.456)

    def test_throws_on_latitude_not_a_number(self):
        with self.assertRaises(exceptions.InvalidFloatXmlParseException):
            dtos.SpatialLocation(latitude='foo', longitude='-23.456')

    def test_throws_on_longitude_not_a_number(self):
        with self.assertRaises(exceptions.InvalidFloatXmlParseException):
            dtos.SpatialLocation(latitude='123.456', longitude='foo')
