class ContentTranslationToolsError(Exception):
    pass

class FieldIDError(ContentTranslationToolsError):
    pass

class MasterInstanceLookupError(ContentTranslationToolsError):
    def __init__(self, message):
        super().__init__(message)

class ModelNotTranslatableError(ContentTranslationToolsError):
    def __init__(self, model):
        self.model = model
        model_name = getattr(model, '__name__', str(model))
        message = "{} is not a TranslatableModel.".format(model_name)
        super().__init__(message)

class FieldNotTranslatableError(ContentTranslationToolsError):
    def __init__(self, field_id):
        self.field_id = field_id
        message = "{} is not a translatable field.".format(field_id)
        super().__init__(message)

class MissingMsgidError(ContentTranslationToolsError):
    def __init__(self):
        message = "Missing msgid."
        super().__init__(message)

class InvalidMsgidError(ContentTranslationToolsError):
    def __init__(self):
        message = "Provided msgid is different from the base translation."
        super().__init__(message)

class ProtectedTranslationError(ContentTranslationToolsError):
    def __init__(self):
        message = "The base translation can not be modified."
        super().__init__(message)

class InvalidContentTypeIDError(ContentTranslationToolsError):
    def __init__(self):
        message = "Invalid content type id."
        super().__init__(message)

class ContentTypeDoesNotExistError(ContentTranslationToolsError):
    def __init__(self):
        message = "Content type matching id does not exist."
        super().__init__(message)

class InvalidInstanceFieldIDError(ContentTranslationToolsError):
    def __init__(self):
        message = "Invalid instance field id."
        super().__init__(message)

class ModelInstanceDoesNotExistError(ContentTranslationToolsError):
    def __init__(self):
        message = "Model instance matching id does not exist."
        super().__init__(message)
