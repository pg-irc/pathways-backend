class CsvParseException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class MissingRequiredFieldCsvParseException(CsvParseException):
    def __init__(self, *args, **kwargs):
        CsvParseException.__init__(self, *args, **kwargs)

class InvalidTypeCsvParseException(CsvParseException):
    def __init__(self, *args, **kwargs):
        CsvParseException.__init__(self, *args, **kwargs)