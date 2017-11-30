from bc211.exceptions import InvalidFloatXmlParseException

def validate_float(float_as_string):
    try:
        return float(float_as_string)
    except ValueError:
        raise InvalidFloatXmlParseException(float_as_string)
