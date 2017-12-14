from django.test import TestCase
from unittest.mock import MagicMock, patch

from django.db import models
from parler.models import TranslatableModel, TranslatedFields
from parler_po.exceptions import (
    FieldNotTranslatableError,
    InvalidMsgidError,
    MasterInstanceLookupError,
    MissingMsgidError,
    ModelNotTranslatableError,
    ProtectedTranslationError
)
from parler_po.translatable_string import TranslatableString
import polib

BASE_LANGUAGE = 'en'

class TestTranslatable(TranslatableModel):
    class Meta:
        app_label = 'parlerpo'
        managed = False

    static = models.CharField(max_length=100)

    translations = TranslatedFields(
        translated_field=models.CharField(max_length=100)
    )

    # Crude hack to mock TranslatableModel database operations

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._mock_translations_dict = {}

    def get_translation(self, language_code):
        translation = self._mock_translations_dict.get(language_code)

        if not translation:
            translation = MagicMock()
            translation.master = self
            translation.language_code = language_code
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

class CreateTranslatableStringTests(TestCase):
    def test_create_with_translatable_model(self):
        translatable = TestTranslatable()
        translatable.id = 1

        base_translation = translatable.get_translation('en')
        base_translation.translated_field = 'translation_msgid'

        translatable_string = TranslatableString(translatable, 'translated_field', 'translation_msgid', 'translation_msgstr')

        self.assertEquals(translatable_string._instance, translatable)
        self.assertEquals(translatable_string._field_id, 'translated_field')
        self.assertEquals(translatable_string._msgid, 'translation_msgid')
        self.assertEquals(translatable_string._msgstr, 'translation_msgstr')

        self.assertEquals(str(translatable_string), 'parlerpo.testtranslatable@translated_field@1')

    def test_create_with_not_translatable_model_raises_error(self):
        not_translatable = TestNotTranslatable()

        with self.assertRaises(ModelNotTranslatableError):
            TranslatableString(not_translatable, 'translated_field', 'translation_msgid', 'translation_msgstr')

    def test_create_with_not_translatable_field_raises_error(self):
        translatable = TestTranslatable()

        with self.assertRaises(FieldNotTranslatableError):
            TranslatableString(translatable, 'static', 'translation_msgid', 'translation_msgstr')

    def test_create_with_invalid_field_raises_error(self):
        translatable = TestTranslatable()

        with self.assertRaises(FieldNotTranslatableError):
            TranslatableString(translatable, 'not_a_field', 'translation_msgid', 'translation_msgstr')

    def test_create_without_msgid_raises_error(self):
        translatable = TestTranslatable()
        translatable.id = 1
        translatable.translated_field = ''

        with self.assertRaises(MissingMsgidError):
            TranslatableString(translatable, 'translated_field', '', 'translation_msgstr')

    def test_create_with_different_msgid_from_base_translation_raises_error(self):
        translatable = TestTranslatable()
        translatable.id = 1
        translatable.translated_field = 'translation_msgid'

        with self.assertRaises(InvalidMsgidError):
            TranslatableString(translatable, 'translated_field', 'not_translation_msgid', 'translation_msgstr')

    def test_create_from_po_entry(self):
        translatable = TestTranslatable()
        translatable.id = 1

        base_translation = translatable.get_translation('en')
        base_translation.translated_field = 'translation_msgid'

        po_entry = polib.POEntry()
        po_entry.occurrences = [
            ('parlerpo.testtranslatable@translated_field@1', None)
        ]
        po_entry.msgid = 'translation_msgid'
        po_entry.msgstr = 'translation_msgstr'

        with patch('parler_po.translatable_string.parse_instance_field_id') as parse_instance_field_id:
            parse_instance_field_id.return_value = (translatable, 'translated_field')
            translatable_string = TranslatableString.from_po_entry(po_entry, po_entry.occurrences[0])
            parse_instance_field_id.assert_called_once_with('parlerpo.testtranslatable@translated_field@1')

        self.assertEquals(translatable_string._instance, translatable)
        self.assertEquals(translatable_string._field_id, 'translated_field')
        self.assertEquals(translatable_string._msgid, 'translation_msgid')
        self.assertEquals(translatable_string._msgstr, 'translation_msgstr')

    def test_create_from_po_entry_with_invalid_occurrence_format_raise_error(self):
        translatable = TestTranslatable()
        translatable.id = 1

        po_entry = polib.POEntry()
        po_entry.occurrences = [
            ('bad format', None)
        ]
        po_entry.msgid = 'translation_msgid'
        po_entry.msgstr = 'translation_msgstr'

        with self.assertRaises(MasterInstanceLookupError):
            TranslatableString.from_po_entry(po_entry, po_entry.occurrences[0])

    def test_create_from_po_entry_with_nonexistent_master_instance_raises_error(self):
        translatable = TestTranslatable()
        translatable.id = 1

        po_entry = polib.POEntry()
        po_entry.occurrences = [
            ('parlerpo.testtranslatable@translated_field@1000', None)
        ]
        po_entry.msgid = 'translation_msgid'
        po_entry.msgstr = 'translation_msgstr'

        with self.assertRaises(MasterInstanceLookupError):
            TranslatableString.from_po_entry(po_entry, po_entry.occurrences[0])

    def test_create_from_po_entry_with_not_translatable_master_instance_raises_error(self):
        translatable = TestNotTranslatable()
        translatable.id = 1

        po_entry = polib.POEntry()
        po_entry.occurrences = [
            ('parlerpo.testnottranslatable@translated_field@1', None)
        ]
        po_entry.msgid = 'translation_msgid'
        po_entry.msgstr = 'translation_msgstr'

        with patch('parler_po.translatable_string.parse_instance_field_id') as parse_instance_field_id:
            parse_instance_field_id.return_value = (translatable, 'translated_field')
            with self.assertRaises(ModelNotTranslatableError):
                TranslatableString.from_po_entry(po_entry, po_entry.occurrences[0])

    def test_create_from_translation(self):
        translatable = TestTranslatable()
        translatable.id = 1

        base_translation = translatable.get_translation(BASE_LANGUAGE)
        base_translation.translated_field = 'translation_msgid'

        translation = translatable.get_translation('fr')
        translation.translated_field = 'translation_msgstr'

        translatable_string = TranslatableString.from_translation(translation, 'translated_field')

        self.assertEquals(translatable_string._instance, translatable)
        self.assertEquals(translatable_string._field_id, 'translated_field')
        self.assertEquals(translatable_string._msgid, 'translation_msgid')
        self.assertEquals(translatable_string._msgstr, 'translation_msgstr')

    def test_create_from_translation_with_missing_msgid_raises_error(self):
        translatable = TestTranslatable()
        translatable.id = 1

        base_translation = translatable.get_translation(BASE_LANGUAGE)
        base_translation.translated_field = ''

        translation = translatable.get_translation('fr')
        translation.translated_field = 'translation_msgstr'

        with self.assertRaises(MissingMsgidError):
            TranslatableString.from_translation(translation, 'translated_field')

class ValidTranslatableStringTests(TestCase):
    def setUp(self):
        self.translatable = TestTranslatable()
        self.translatable.id = 1

        self.base_translation = self.translatable.get_translation(BASE_LANGUAGE)
        self.base_translation.translated_field = 'translation_msgid'

        self.translatable_string = TranslatableString(
            self.translatable, 'translated_field', 'translation_msgid', 'translation_msgstr'
        )

    def test_as_po_entry(self):
        po_entry = self.translatable_string.as_po_entry()

        self.assertEquals(po_entry.msgid, 'translation_msgid')
        self.assertEquals(po_entry.msgstr, 'translation_msgstr')
        self.assertEquals(po_entry.occurrences, [
            ('parlerpo.testtranslatable@{}@{}'.format('translated_field', 1), None)
        ])

    def test_save_new_translation(self):
        modified = self.translatable_string.save_translation('fr')
        translation = self.translatable.get_translation('fr')

        translation.save.assert_called_once_with()

        self.assertTrue(modified)
        self.assertEquals(translation.master, self.translatable)
        self.assertEquals(translation.translated_field, 'translation_msgstr')

    def test_save_translation_without_changes_returns_false(self):
        self.translatable_string.save_translation('fr')
        translation = self.translatable.get_translation('fr')
        translation.save.reset_mock()

        modified = self.translatable_string.save_translation('fr')

        translation.save.assert_not_called()
        self.assertFalse(modified)

    def test_save_translation_with_base_translation_raises_error(self):
        with self.assertRaises(ProtectedTranslationError):
            self.translatable_string.save_translation(BASE_LANGUAGE)

        self.base_translation.save.assert_not_called()
