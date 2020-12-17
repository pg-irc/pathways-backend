class XmlParseException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class InvalidFloatXmlParseException(XmlParseException):
    def __init__(self, *args, **kwargs):
        XmlParseException.__init__(self, *args, **kwargs)


class InvalidNestedObjectXmlParseException(XmlParseException):
    def __init__(self, *args, **kwargs):
        XmlParseException.__init__(self, *args, **kwargs)


class MissingRequiredFieldXmlParseException(XmlParseException):
    def __init__(self, *args, **kwargs):
        XmlParseException.__init__(self, *args, **kwargs)


class InvalidTypeXmlParseException(XmlParseException):
    def __init__(self, *args, **kwargs):
        XmlParseException.__init__(self, *args, **kwargs)
