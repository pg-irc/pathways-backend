import logging
from urllib import parse as urlparse
from datetime import datetime
from django.core import validators
from django.core.exceptions import ValidationError
from bc211.parser import remove_double_escaped_html_markup, clean_one_phone_number
from bc211.open_referral_csv_import import exceptions

LOGGER = logging.getLogger(__name__)


def parse_required_field_with_double_escaped_html(field, value):
    required_value = parse_required_field(field, value)
    return remove_double_escaped_html_markup(required_value)


def parse_alternate_name(value):
    alternate_name = parse_optional_field(value)
    return remove_double_escaped_html_markup(alternate_name)


def parse_description(value):
    description = parse_optional_field(value)
    return remove_double_escaped_html_markup(description)


def parse_email(active_record_id, value):
    email = parse_optional_field(value)
    if csv_value_is_empty(email):
        return None
    cleaned_email = remove_double_escaped_html_markup(email)
    return validated_email_or_none(active_record_id, cleaned_email)


def validated_email_or_none(active_record_id, email):
    try:
        validators.validate_email(email)
        return email
    except ValidationError:
        LOGGER.warning('The record with the id: "%s" has an invalid email.', active_record_id)
        return None


def parse_last_verified_date(value):
    last_verified_date = parse_optional_field(value)
    if last_verified_date is None or value == '':
        return None
    return datetime.strptime(last_verified_date, '%Y-%m-%d')


def parse_required_type(value):
    required_type = parse_required_field('type', value)
    return remove_double_escaped_html_markup(required_type)


def parse_attention(value):
    attention = parse_optional_field(value)
    return remove_double_escaped_html_markup(attention)


def parse_addresses(addresses_from_csv):
    addresses = [parse_address(address) for address in addresses_from_csv]
    non_empty_addresses = [address for address in addresses if address]
    return '\n'.join(non_empty_addresses)


def parse_address(value):
    address = parse_optional_field(value)
    return remove_double_escaped_html_markup(address)


def parse_city(value):
    city = parse_optional_field(value)
    return remove_double_escaped_html_markup(city)


def parse_state_province(value):
    state_province = parse_optional_field(value)
    return remove_double_escaped_html_markup(state_province)


def parse_postal_code(value):
    postal_code = parse_optional_field(value)
    return remove_double_escaped_html_markup(postal_code)


def parse_country(value):
    country = parse_required_field('country', value)
    cleaned_country = remove_double_escaped_html_markup(country)
    return two_letter_country_code_or_none(cleaned_country)


def two_letter_country_code_or_none(country):
    if country == 'Canada':
        return 'CA'
    if country == 'United States':
        return 'US'
    if len(country) > 2:
        raise exceptions.InvalidFieldCsvParseException(
            'Country field with value: {} is invalid'.format(country)
        )
    return country


def parse_phone_number(value):
    phone_number = parse_required_field('number', value)
    phone_number_without_markup = remove_double_escaped_html_markup(phone_number)
    return clean_one_phone_number(phone_number_without_markup)


def parse_taxonomy_id(value):
    taxonomy_id = parse_required_field('taxonomy_id', value)
    return remove_double_escaped_html_markup(taxonomy_id)


def parse_required_field(field, value):
    if csv_value_is_empty(value):
        raise exceptions.MissingRequiredFieldCsvParseException(
            'Missing required field: "{0}"'.format(field)
        )
    return value


def parse_optional_field(value):
    if csv_value_is_empty(value):
        return ''
    return value


def parse_website_with_prefix(active_record_id, value):
    website = parse_optional_field(value)
    if csv_value_is_empty(website):
        return None
    website_with_http_prefix = add_http_prefix_to_website(website)
    return validated_website_or_none(active_record_id, website_with_http_prefix)


def validated_website_or_none(active_record_id, website):
    validate_url = validators.URLValidator()
    try:
        validate_url(website)
        return website
    except ValidationError:
        LOGGER.warning('The record with the id: "%s" has an invalid URL.', active_record_id)
        return None


def add_http_prefix_to_website(website):
    parts = urlparse.urlparse(website, 'http')
    whole_with_extra_slash = urlparse.urlunparse(parts)
    return whole_with_extra_slash.replace('///', '//')


def parse_coordinate_if_defined(value):
    coordinate = parse_optional_field(value)
    return None if csv_value_is_empty(value) else float(coordinate)


def csv_value_is_empty(value):
    return value is None or value == ''
