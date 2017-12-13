class TranslatableStringError(Exception):
    pass

class MasterInstanceLookupError(TranslatableStringError):
    def __init__(self, message):
        super().__init__(message)

class ModelNotTranslatableError(TranslatableStringError):
    def __init__(self, model):
        self.model = model
        message = "{} is not a TranslatableModel".format(model.__name__)
        super().__init__(message)

class FieldNotTranslatableError(TranslatableStringError):
    def __init__(self, field_id):
        self.field_id = field_id
        message = "{} is not a translatable field".format(field_id)
        super().__init__(message)

class MissingMsgidError(TranslatableStringError):
    def __init__(self):
        message = "Missing msgid"
        super().__init__(message)

class InvalidMsgidError(TranslatableStringError):
    def __init__(self):
        message = "Provided msgid does not match the base translation"
        super().__init__(message)

class ProtectedTranslationError(TranslatableStringError):
    def __init__(self):
        message = "The base translation can not be modified"
        super().__init__(message)
