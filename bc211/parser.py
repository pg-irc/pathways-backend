from bc211 import dtos
from bc211.exceptions import MissingRequiredFieldXmlParseException
from urllib import parse as urlparse
import itertools
import logging
import re
import xml.etree.ElementTree as etree

LOGGER = logging.getLogger(__name__)

BC211_JSON_RE = r"(\w+)\:\'([^\']+)\'"

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
    services = parse_services(site, id)
    LOGGER.info('Parsed location: %s %s', id, name)
    return dtos.Location(id=id, name=name, organization_id=organization_id,
                         description=description, spatial_location=spatial_location,
                         services=services)

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

def parse_services(site, site_id):
    services = site.findall('SiteService')
    return map(ServiceParser(site_id), services)

class ServiceParser:
    def __init__(self, site_id):
        self.site_id = site_id

    def __call__(self, service):
        return parse_service(service, self.site_id)

def parse_service(service, site_id):
    id = parse_service_id(service)
    name = parse_service_name(service)
    taxonomy_terms = parse_service_taxonomy_terms(service, id)
    LOGGER.info('Parsed service: %s %s', id, name)
    return dtos.Service(id=id, name=name, site_id=site_id, taxonomy_terms=taxonomy_terms)

def parse_service_id(service):
    return parse_required_field(service, 'Key')

def parse_service_name(service):
    return parse_required_field(service, 'Name')

def parse_service_taxonomy_terms(service, service_id):
    taxonomy_terms = service.findall('Taxonomy')
    return itertools.chain.from_iterable(
        map(ServiceTaxonomyTermParser(service_id), taxonomy_terms)
    )

class ServiceTaxonomyTermParser:
    def __init__(self, service_id):
        self.service_id = service_id

    def __call__(self, service_taxonomy_term):
        return parse_service_taxonomy_term(service_taxonomy_term, self.service_id)

def parse_service_taxonomy_term(service_taxonomy_term, service_id):
    code = parse_required_field(service_taxonomy_term, 'Code')

    LOGGER.info('Parsed taxonomy term: %s %s', id, code)

    if code and is_bc211_taxonomy_term(code):
        yield from parse_bc211_taxonomy_term(code)
    elif code:
        yield from parse_airs_taxonomy_term(code)

def is_bc211_taxonomy_term(code_str):
    return code_str.startswith('{')

def parse_bc211_taxonomy_term(code_str):
    groups = re.findall(BC211_JSON_RE, code_str)
    for (vocabulary, name) in groups:
        full_vocabulary = 'bc211-{}'.format(vocabulary)
        yield dtos.TaxonomyTerm(vocabulary=full_vocabulary, name=name)

def parse_airs_taxonomy_term(code_str):
    vocabulary = 'airs'
    yield dtos.TaxonomyTerm(vocabulary=vocabulary, name=code_str)
