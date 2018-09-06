import unittest
from bc211 import dtos, exceptions
from common.testhelpers.random_test_values import a_string, a_phone_number

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

    def test_can_create_with_none_value_for_services(self):
        services = None
        location = dtos.Location(id=a_string(), name=a_string(),
                                 organization_id=a_string(), services=services)
        self.assertEqual(location.services, services)

    def test_can_create_with_list_of_service_dtos_for_services(self):
        service = dtos.Service(id=a_string(), name=a_string(),
                               organization_id=a_string(), site_id=a_string())
        services = [service]
        location = dtos.Location(id=a_string(), name=a_string(),
                                 organization_id=a_string(), services=services)
        self.assertEqual(location.services, services)

    def test_throws_on_single_service_for_services(self):
        service = dtos.Service(id=a_string(), name=a_string(),
                               organization_id=a_string(), site_id=a_string())
        with self.assertRaises(exceptions.InvalidTypeXmlParseException):
            dtos.Location(id=a_string(), name=a_string(),
                          organization_id=a_string(), services=service)

    def test_throws_on_list_of_wrong_type_for_services(self):
        services = [a_string()]
        with self.assertRaises(exceptions.InvalidTypeXmlParseException):
            dtos.Location(id=a_string(), name=a_string(),
                          organization_id=a_string(), services=services)

    def test_can_create_with_none_value_for_phone_numbers(self):
        phone_numbers = None
        location = dtos.Location(id=a_string(), name=a_string(),
                                 organization_id=a_string(), phone_numbers=phone_numbers)
        self.assertEqual(location.services, phone_numbers)

    def test_can_create_with_list_of_phone_at_location_dtos_for_phone_numbers(self):
        phone_at_location = dtos.PhoneAtLocation(location_id=a_string(),
                                                 phone_number_type_id=a_string(),
                                                 phone_number=a_phone_number())
        phones_at_location = [phone_at_location]
        location = dtos.Location(id=a_string(), name=a_string(),
                                 organization_id=a_string(), phone_numbers=phones_at_location)
        self.assertEqual(location.phone_numbers, phones_at_location)

    def test_throws_on_single_phone_at_location_for_phone_numbers(self):
        phone_at_location = dtos.PhoneAtLocation(location_id=a_string(),
                                                 phone_number_type_id=a_string(),
                                                 phone_number=a_phone_number())
        with self.assertRaises(exceptions.InvalidTypeXmlParseException):
            dtos.Location(id=a_string(), name=a_string(),
                          organization_id=a_string(), phone_numbers=phone_at_location)

    def test_throws_on_list_of_wrong_type_for_phone_numbers(self):
        phone_numbers = [a_string()]
        with self.assertRaises(exceptions.InvalidTypeXmlParseException):
            dtos.Location(id=a_string(), name=a_string(),
                          organization_id=a_string(), phone_numbers=phone_numbers)


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


class TestService(unittest.TestCase):
    def test_can_create(self):
        service = dtos.Service(id='id', name='name', organization_id='organization_id', site_id='site_id', description='description')
        self.assertEqual(service.id, 'id')
        self.assertEqual(service.name, 'name')
        self.assertEqual(service.organization_id, 'organization_id')
        self.assertEqual(service.site_id, 'site_id')
        self.assertEqual(service.description, 'description')

    def test_throws_on_missing_id(self):
        with self.assertRaises(exceptions.MissingRequiredFieldXmlParseException):
            dtos.TaxonomyTerm(name='name', organization_id='organization_id',
                              site_id='site_id', description='description')

    def test_throws_on_missing_name(self):
        with self.assertRaises(exceptions.MissingRequiredFieldXmlParseException):
            dtos.TaxonomyTerm(id='id', organization_id='organization_id',
                              site_id='site_id', description='description')

    def test_throws_on_missing_organization_id(self):
        with self.assertRaises(exceptions.MissingRequiredFieldXmlParseException):
            dtos.TaxonomyTerm(id='id', name='name', site_id='site_id', description='description')

    def test_throws_on_missing_site_id(self):
        with self.assertRaises(exceptions.MissingRequiredFieldXmlParseException):
            dtos.TaxonomyTerm(id='id', name='name',
                              organization_id='organization_id', description='description')

class TestTaxonomyTerm(unittest.TestCase):
    def test_can_create(self):
        taxonomy_term = dtos.TaxonomyTerm(taxonomy_id='taxonomy_id', name='name')
        self.assertEqual(taxonomy_term.taxonomy_id, 'taxonomy_id')
        self.assertEqual(taxonomy_term.name, 'name')

    def test_throws_on_missing_taxonomy_id(self):
        with self.assertRaises(exceptions.MissingRequiredFieldXmlParseException):
            dtos.TaxonomyTerm(name='name')

    def test_throws_on_missing_name(self):
        with self.assertRaises(exceptions.MissingRequiredFieldXmlParseException):
            dtos.TaxonomyTerm(taxonomy_id='taxonomy_id')

class PhoneAtLocation(unittest.TestCase):
    def test_can_create(self):
        location_id = a_string()
        phone_number_type_id = a_string()
        phone_number = a_phone_number()
        phone_at_location = dtos.PhoneAtLocation(location_id=location_id,
                                                 phone_number_type_id=phone_number_type_id,
                                                 phone_number=phone_number)
        self.assertEqual(phone_at_location.location_id, location_id)
        self.assertEqual(phone_at_location.phone_number_type_id, phone_number_type_id)
        self.assertEqual(phone_at_location.phone_number, phone_number)

    def test_throws_on_missing_location_id(self):
        with self.assertRaises(exceptions.MissingRequiredFieldXmlParseException):
            dtos.PhoneAtLocation(phone_number_type_id=a_string(), phone_number=a_phone_number())

    def test_throws_on_missing_phone_number_type_id(self):
        with self.assertRaises(exceptions.MissingRequiredFieldXmlParseException):
            dtos.PhoneAtLocation(phone_number=a_phone_number(), location_id=a_string())

    def test_throws_on_phone_number(self):
        with self.assertRaises(exceptions.MissingRequiredFieldXmlParseException):
            dtos.PhoneAtLocation(phone_number_type_id=a_string(), location_id=a_string())
