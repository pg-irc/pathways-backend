from bc211.parser import remove_double_escaped_html_markup
from urllib import parse as urlparse
from .exceptions import MissingRequiredFieldCsvParseException
from datetime import datetime


def parse_organization_id(value):
    organization_id = parse_required_field('organization_id', value)
    return remove_double_escaped_html_markup(organization_id)


def parse_service_id(value):
    service_id = parse_required_field('service_id', value)
    return remove_double_escaped_html_markup(service_id)


def parse_location_id(value):
    location_id = parse_required_field('location_id', value)
    return remove_double_escaped_html_markup(location_id)


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


def parse_last_verified_date(value):
    last_verified_date = parse_optional_field('last_verified_date', value)
    if last_verified_date is None or value == '':
        return None
    return datetime.strptime(last_verified_date, '%d-%m-%Y')


def parse_required_type(value):
    required_type = parse_required_field('type', value)
    return remove_double_escaped_html_markup(required_type)


def parse_attention(value):
    attention = parse_optional_field('attention', value)
    return remove_double_escaped_html_markup(attention)


def parse_address(value):
    address = parse_optional_field('address',value)
    return remove_double_escaped_html_markup(address)


def parse_city(value):
    city = parse_required_field('city', value)
    return remove_double_escaped_html_markup(city)


def parse_state_province(value):
    state_province = parse_optional_field('state_province', value)
    return remove_double_escaped_html_markup(state_province)


def parse_postal_code(value):
    postal_code = parse_optional_field('postal_code', value)
    return remove_double_escaped_html_markup(postal_code)


def parse_country(value):
    country = parse_required_field('country', value)
    return remove_double_escaped_html_markup(country)


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