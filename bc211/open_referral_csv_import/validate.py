from .exceptions import MissingRequiredFieldCsvParseException, InvalidTypeCsvParseException, InvalidNestedObjectCsvParseException, InvalidFloatCsvParseException


def required_string(field, values):
    value = values.get(field)
    if isinstance(value, str):
        return value
    raise MissingRequiredFieldCsvParseException(field)


def optional_string(field, values):
    value = values.get(field)
    if value is None or isinstance(value, str):
        return value
    raise InvalidTypeCsvParseException(field)


def optional_object(the_class, field, values):
    value = values.get(field)
    if value is None or isinstance(value, the_class):
        return value
    raise InvalidNestedObjectCsvParseException(field)


def required_float(field, values):
    value = values.get(field)
    return parse_float(value)


def parse_float(value):
    try:
        return float(value)
    except ValueError:
        raise InvalidFloatCsvParseException(value)