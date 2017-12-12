from bc211 import exceptions

def required_string(field, values):
    value = values.get(field)
    if isinstance(value, str):
        return value
    raise exceptions.MissingRequiredFieldXmlParseException(field)

def optional_string(field, values):
    value = values.get(field)
    if value is None or isinstance(value, str):
        return value
    raise exceptions.InvalidNestedObjectXmlParseException(field)

def optional_object(the_class, field, values):
    value = values.get(field)
    if value is None or isinstance(value, the_class):
        return value
    raise exceptions.InvalidNestedObjectXmlParseException(field)

def required_float(field, values):
    value = values.get(field)
    return parse_float(value)

def parse_float(value):
    try:
        return float(value)
    except ValueError:
        raise exceptions.InvalidFloatXmlParseException(value)
