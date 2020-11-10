from bc211.parser import remove_double_escaped_html_markup
from urllib import parse as urlparse
from .exceptions import MissingRequiredFieldCsvParseException


def parse_organization_id(value):
    organization_id = parse_required_field('organization_id', value)
    return remove_double_escaped_html_markup(organization_id)


def parse_service_id(value):
    service_id = parse_required_field('service_id', value)
    return remove_double_escaped_html_markup(service_id)


def parse_name(value):
    name = parse_required_field('name', value)
    return remove_double_escaped_html_markup(name)


def parse_alternate_name(value):
    alternate_name = parse_optional_field('alternate_name', value)
    return remove_double_escaped_html_markup(alternate_name)


def parse_description(value):
    description = parse_optional_field('description', value)
    return remove_double_escaped_html_markup(description)


def parse_email(value):
    email = parse_optional_field('email', value)
    return remove_double_escaped_html_markup(email)


def parse_required_field(field, value):
    if csv_value_is_empty(value):
        raise MissingRequiredFieldCsvParseException('Missing required field: "{0}"'.format(field))
    return value

# TODO remove field argument

def parse_optional_field(field, value):
    if csv_value_is_empty(value):
        return None
    return value


def parse_website_with_prefix(field, value):
    website = parse_optional_field(field, value)
    return None if csv_value_is_empty(value) else website_with_http_prefix(website)


def website_with_http_prefix(website):
    parts = urlparse.urlparse(website, 'http')
    whole_with_extra_slash = urlparse.urlunparse(parts)
    return whole_with_extra_slash.replace('///', '//')

def parse_coordinate_if_defined(field, value):
    coordinate = parse_optional_field(field, value)
    return None if csv_value_is_empty(value) else float(coordinate)

def csv_value_is_empty(value):
    return value is None or value == ''