class CsvParseException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class MissingRequiredFieldCsvParseException(CsvParseException):
    def __init__(self, *args, **kwargs):
        CsvParseException.__init__(self, *args, **kwargs)


class InvalidFieldCsvParseException(CsvParseException):
    def __init__(self, *args, **kwargs):
        CsvParseException.__init__(self, *args, **kwargs)


class CsvImportException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class InvalidFileCsvImportException(CsvImportException):
    def __init__(self, *args, **kwargs):
        CsvImportException.__init__(self, *args, **kwargs)