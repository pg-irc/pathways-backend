import unittest
import xml.etree.ElementTree as etree
from bc211 import parser

ONE_AGENCY_FIXTURE = 'bc211/data/BC211_data_one_agency.xml'
MULTI_AGENCY_FIXTURE = 'bc211/data/BC211_data_excerpt.xml'

class BC211ParserTests(unittest.TestCase):
    def test_parse_many_service_providers(self):
        file_open_for_reading = open(MULTI_AGENCY_FIXTURE, 'r')
        xml = file_open_for_reading.read()
        parser_result = parser.parse(xml)
        self.assertEqual(len(list(parser_result.service_providers)), 16)
        self.assertEqual(len(list(parser_result.organizations)), 16)


class OrganizationParserTests(unittest.TestCase):
    def setUp(self):
        file_open_for_reading = open(ONE_AGENCY_FIXTURE, 'r')
        xml = file_open_for_reading.read()
        root = etree.fromstring(xml)
        agency_xml = root.find('Agency')
        self.organization = parser.parse_organization(agency_xml)

    def test_can_parse_id(self):
        self.assertEqual(self.organization.id, '9487364')

    def test_can_parse_name(self):
        self.assertEqual(self.organization.name, 'Langley Child Development Centre')

    def test_can_parse_description(self):
        self.assertEqual(self.organization.description[:30], 'Provides inclusive, family-cen')

    def test_can_parse_website(self):
        self.assertEqual(self.organization.website, 'http://www.langleycdc.com')

    def test_can_parse_email(self):
        self.assertEqual(self.organization.email, 'info@langleycdc.com')


class ServiceProviderParserTests(unittest.TestCase):
    def setUp(self):
        file_open_for_reading = open(ONE_AGENCY_FIXTURE, 'r')
        xml = file_open_for_reading.read()
        root = etree.fromstring(xml)
        provider = root.find('Agency')
        self.service_provider = parser.parse_service_provider(provider)

    def test_can_parse_name(self):
        self.assertEqual(self.service_provider.name, 'Langley Child Development Centre')

    def test_can_parse_description(self):
        self.assertEqual(self.service_provider.description[:30], 'Provides inclusive, family-cen')

    def test_can_parse_latitude(self):
        self.assertAlmostEqual(self.service_provider.spatial_location.latitude, 49.087284)

    def test_can_parse_longitude(self):
        self.assertAlmostEqual(self.service_provider.spatial_location.longitude, -122.607918)
