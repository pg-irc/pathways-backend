from bc211.parser import remove_double_escaped_html_markup
from urllib import parse as urlparse
from .exceptions import MissingRequiredFieldCsvParseException


def parse_required_field(field, value):
    try:
        return remove_double_escaped_html_markup(value)
    except AttributeError:
        raise MissingRequiredFieldCsvParseException('Missing required field: "{0}"'.format(field))


def parse_optional_field(field, value):
    if value is None:
        return None
    return remove_double_escaped_html_markup(value)


def parse_website_with_prefix(field, value):
    website = parse_optional_field(field, value)
    return None if website is None else website_with_http_prefix(website)


def website_with_http_prefix(website):
    parts = urlparse.urlparse(website, 'http')
    whole_with_extra_slash = urlparse.urlunparse(parts)
    return whole_with_extra_slash.replace('///', '//')