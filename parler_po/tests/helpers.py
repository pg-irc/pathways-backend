from django.db import models
from parler.models import TranslatableModel, TranslatedFields
from unittest.mock import MagicMock

BASE_LANGUAGE = 'en'

class TestTranslatable(TranslatableModel):
    class Meta:
        app_label = 'parlerpo'
        managed = False

    static = models.CharField(max_length=100)

    translations = TranslatedFields(
        translated_field_1=models.CharField(max_length=100),
        translated_field_2=models.CharField(max_length=100),
        translated_field_3=models.CharField(max_length=100)
    )

    def with_base_translation(self, **fields):
        return self.with_translation(BASE_LANGUAGE, **fields)

    def with_translation(self, language_code, **fields):
        translation = self.get_translation(language_code)
        for field_name, value in fields.items():
            setattr(translation, field_name, value)
        return self

    def get_base_translation(self):
        return self.get_translation(BASE_LANGUAGE)

    # Crude hacks to mock TranslatableModel database operations

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._mock_translations_dict = {}

    def get_translation(self, language_code):
        translation = self._mock_translations_dict.get(language_code)

        if not translation:
            translation = MagicMock()
            translation.master = self
            translation.language_code = language_code
            translation.get_translated_fields.return_value = [
                'translated_field_1',
                'translated_field_2',
                'translated_field_3'
            ]
            self._mock_translations_dict[language_code] = translation

        return translation

    def create_translation(self, language_code):
        self.get_translation(language_code)

    def has_translation(self, language_code):
        return language_code in self._mock_translations_dict

class TestNotTranslatable(models.Model):
    class Meta:
        app_label = 'parlerpo'
        managed = False
