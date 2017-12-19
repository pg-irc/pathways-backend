from organizations.models import Organization

BASE_LANGUAGE = 'en'

class OrganizationBuilder(object):
    model = Organization

    def __init__(self, **kwargs):
        self.instance = self.model(**kwargs)
        self.instance.save()

    def with_base_translation(self, **fields):
        return self.with_translation(BASE_LANGUAGE, **fields)

    def with_translation(self, language_code, **fields):
        if not self.instance.has_translation(language_code):
            self.instance.create_translation(language_code)

        translation = self.instance.get_translation(language_code)

        for field_name, value in fields.items():
            setattr(translation, field_name, value)

        translation.save()

        return self

    def build(self):
        return self.instance
