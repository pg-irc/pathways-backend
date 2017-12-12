import logging
import xml.etree.ElementTree as etree
from urllib import parse as urlparse
from bc211 import dtos
from bc211.exceptions import MissingRequiredFieldXmlParseException

LOGGER = logging.getLogger(__name__)

def read_records_from_file(file):
    xml = file.read()
    return parse(xml)

def parse(xml_data_as_string):
    root_xml = etree.fromstring(xml_data_as_string)
    agencies = root_xml.findall('Agency')
    return map(parse_agency, agencies)

def parse_agency(agency):
    id = parse_agency_key(agency)
    name = parse_agency_name(agency)
    description = parse_agency_description(agency)
    website = parse_agency_website_with_prefix(agency)
    email = parse_agency_email(agency)
    LOGGER.info('Parsed organization: %s %s', id, name)
    locations = parse_sites(agency, id)
    return dtos.Organization(id=id, name=name, description=description, website=website,
                             email=email, locations=locations)

def parse_agency_key(agency):
    return parse_required_field(agency, 'Key')

def parse_required_field(parent, field):
    try:
        return parent.find(field).text
    except AttributeError:
        raise MissingRequiredFieldXmlParseException(field)

def parse_optional_field(parent, field):
    value = parent.find(field)
    return None if value is None else value.text

def parse_agency_name(agency):
    return parse_required_field(agency, 'Name')

def parse_agency_description(agency):
    return parse_required_field(agency, 'AgencyDescription')

def parse_agency_email(agency):
    return parse_optional_field(agency, 'Email/Address')

def parse_agency_website_with_prefix(agency):
    website = parse_optional_field(agency, 'URL/Address')
    return None if website is None else website_with_http_prefix(website)

def website_with_http_prefix(website):
    parts = urlparse.urlparse(website, 'http')
    whole_with_extra_slash = urlparse.urlunparse(parts)
    return whole_with_extra_slash.replace('///', '//')

def parse_sites(agency, organization_id):
    sites = agency.findall('Site')
    return map(SiteParser(organization_id), sites)

class SiteParser:
    def __init__(self, organization_id):
        self.organization_id = organization_id

    def __call__(self, site):
        return parse_site(site, self.organization_id)

def parse_site(site, organization_id):
    id = parse_site_id(site)
    name = parse_site_name(site)
    description = parse_site_description(site)
    spatial_location = parse_spatial_location_if_defined(site)
    LOGGER.info('Parsed location: %s %s', id, name)
    return dtos.Location(id=id, name=name, organization_id=organization_id,
                         description=description, spatial_location=spatial_location)

def parse_site_id(site):
    return parse_required_field(site, 'Key')

def parse_site_name(site):
    return parse_required_field(site, 'Name')

def parse_site_description(site):
    return parse_required_field(site, 'SiteDescription')

def parse_spatial_location_if_defined(site):
    latitude = parse_optional_field(site, 'SpatialLocation/Latitude')
    longitude = parse_optional_field(site, 'SpatialLocation/Longitude')
    if latitude is None or longitude is None:
        return None
    return dtos.SpatialLocation(latitude=latitude, longitude=longitude)
