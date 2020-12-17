import logging
from urllib import parse as urlparse
from datetime import datetime
from bc211.import_xml.parser import remove_double_escaped_html_markup, clean_one_phone_number
from bc211.open_referral_csv_import import exceptions
from django.core import validators
from django.core.exceptions import ValidationError

LOGGER = logging.getLogger(__name__)


def parse_required_field_with_double_escaped_html(field, value):
    required_value = parse_required_field(field, value)
    return remove_double_escaped_html_markup(required_value)


def parse_optional_field_with_double_escaped_html(value):
    optional_value = parse_optional_field(value)
    return remove_double_escaped_html_markup(optional_value)


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
        LOGGER.debug('The record with the id: "%s" has an invalid email.', active_record_id)
        return None


def parse_last_verified_date(value):
    last_verified_date = parse_optional_field(value)
    if last_verified_date is None or value == '':
        return None
    return datetime.strptime(last_verified_date, '%Y-%m-%d')


def parse_addresses(addresses_from_csv):
    addresses = [
        parse_optional_field_with_double_escaped_html(address) for address in addresses_from_csv
    ]
    non_empty_addresses = [address for address in addresses if address]
    return '\n'.join(non_empty_addresses)


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
        LOGGER.debug('The record with the id: "%s" has an invalid URL.', active_record_id)
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
