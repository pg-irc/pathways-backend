from .exceptions import MissingRequiredFieldCsvParseException, InvalidTypeCsvParseException


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