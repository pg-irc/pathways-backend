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
        foo=models.CharField(max_length=100)
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
    def test_create__translatable(self):
        translatable = TestTranslatable()
        translatable.id = 1

        base_translation = translatable.get_translation('en')
        base_translation.foo = 'bar'

        translatable_string = TranslatableString(translatable, 'foo', 'bar', 'baz')

        self.assertEquals(translatable_string._instance, translatable)
        self.assertEquals(translatable_string._field_id, 'foo')
        self.assertEquals(translatable_string._msgid, 'bar')
        self.assertEquals(translatable_string._msgstr, 'baz')

        self.assertEquals(str(translatable_string), 'parlerpo.testtranslatable@foo@1')

    def test_create__not_translatable(self):
        not_translatable = TestNotTranslatable()

        with self.assertRaises(ModelNotTranslatableError):
            TranslatableString(not_translatable, 'foo', 'bar', 'baz')

    def test_create__static_field(self):
        translatable = TestTranslatable()

        with self.assertRaises(FieldNotTranslatableError):
            TranslatableString(translatable, 'static', 'bar', 'baz')

    def test_create__invalid_field(self):
        translatable = TestTranslatable()

        with self.assertRaises(FieldNotTranslatableError):
            TranslatableString(translatable, 'not_a_field', 'bar', 'baz')

    def test_create__invalid_msgid(self):
        translatable = TestTranslatable()
        translatable.id = 1
        translatable.foo = 'not_bar'

        with self.assertRaises(InvalidMsgidError):
            TranslatableString(translatable, 'foo', 'bar', 'baz')

    def test_create__missing_msgid(self):
        translatable = TestTranslatable()
        translatable.id = 1
        translatable.foo = ''

        with self.assertRaises(MissingMsgidError):
            TranslatableString(translatable, 'foo', '', 'baz')

    def test_create_from_po_entry(self):
        translatable = TestTranslatable()
        translatable.id = 1

        base_translation = translatable.get_translation('en')
        base_translation.foo = 'bar'

        po_entry = polib.POEntry()
        po_entry.occurrences = [
            ('parlerpo.testtranslatable@foo@1', None)
        ]
        po_entry.msgid = 'bar'
        po_entry.msgstr = 'baz'

        with patch('parler_po.translatable_string.parse_instance_field_id') as parse_instance_field_id:
            parse_instance_field_id.return_value = (translatable, 'foo')
            translatable_string = TranslatableString.from_po_entry(po_entry, po_entry.occurrences[0])
            parse_instance_field_id.assert_called_once_with('parlerpo.testtranslatable@foo@1')

        self.assertEquals(translatable_string._instance, translatable)
        self.assertEquals(translatable_string._field_id, 'foo')
        self.assertEquals(translatable_string._msgid, 'bar')
        self.assertEquals(translatable_string._msgstr, 'baz')

    def test_create_from_nonexistent_po_entry_occurrence(self):
        translatable = TestTranslatable()
        translatable.id = 1

        po_entry = polib.POEntry()
        po_entry.occurrences = [
            ('parlerpo.testtranslatable@foo@1000', None)
        ]
        po_entry.msgid = 'bar'
        po_entry.msgstr = 'baz'

        with self.assertRaises(MasterInstanceLookupError):
            TranslatableString.from_po_entry(po_entry, po_entry.occurrences[0])

    def test_create_from_invalid_po_entry_occurrence(self):
        translatable = TestTranslatable()
        translatable.id = 1

        po_entry = polib.POEntry()
        po_entry.occurrences = [
            ('bad format', None)
        ]
        po_entry.msgid = 'bar'
        po_entry.msgstr = 'baz'

        with self.assertRaises(MasterInstanceLookupError):
            TranslatableString.from_po_entry(po_entry, po_entry.occurrences[0])

    def test_create_from_po_entry__not_translatable(self):
        translatable = TestNotTranslatable()
        translatable.id = 1

        po_entry = polib.POEntry()
        po_entry.occurrences = [
            ('parlerpo.testnottranslatable@foo@1', None)
        ]
        po_entry.msgid = 'bar'
        po_entry.msgstr = 'baz'

        with patch('parler_po.translatable_string.parse_instance_field_id') as parse_instance_field_id:
            parse_instance_field_id.return_value = (translatable, 'foo')
            with self.assertRaises(ModelNotTranslatableError):
                TranslatableString.from_po_entry(po_entry, po_entry.occurrences[0])

    def test_create_from_translation(self):
        translatable = TestTranslatable()
        translatable.id = 1

        base_translation = translatable.get_translation(BASE_LANGUAGE)
        base_translation.foo = 'bar'

        translation = translatable.get_translation('fr')
        translation.foo = 'baz'

        translatable_string = TranslatableString.from_translation(translation, 'foo')

        self.assertEquals(translatable_string._instance, translatable)
        self.assertEquals(translatable_string._field_id, 'foo')
        self.assertEquals(translatable_string._msgid, 'bar')
        self.assertEquals(translatable_string._msgstr, 'baz')

    def test_create_from_translation__missing_msgid(self):
        translatable = TestTranslatable()
        translatable.id = 1

        base_translation = translatable.get_translation(BASE_LANGUAGE)
        base_translation.foo = ''

        translation = translatable.get_translation('fr')
        translation.foo = 'baz'

        with self.assertRaises(MissingMsgidError):
            TranslatableString.from_translation(translation, 'foo')

class ValidTranslatableStringTests(TestCase):
    TRANSLATION_FIELD = 'foo'
    TRANSLATION_MSGID = 'bar'
    TRANSLATION_MSGSTR = 'baz'
    TRANSLATABLE_ID = 1

    def setUp(self):
        self.translatable = TestTranslatable()
        self.translatable.id = self.TRANSLATABLE_ID

        self.base_translation = self.translatable.get_translation(BASE_LANGUAGE)
        self.base_translation.foo = self.TRANSLATION_MSGID

        self.translatable_string = TranslatableString(
            self.translatable, self.TRANSLATION_FIELD, self.TRANSLATION_MSGID, self.TRANSLATION_MSGSTR
        )

    def test_as_po_entry(self):
        po_entry = self.translatable_string.as_po_entry()

        self.assertEquals(po_entry.msgid, self.TRANSLATION_MSGID)
        self.assertEquals(po_entry.msgstr, self.TRANSLATION_MSGSTR)
        self.assertEquals(po_entry.occurrences, [
            ('parlerpo.testtranslatable@{}@{}'.format(self.TRANSLATION_FIELD, self.TRANSLATABLE_ID), None)
        ])

    def test_save_new_translation(self):
        modified = self.translatable_string.save_translation('fr')
        translation = self.translatable.get_translation('fr')

        translation.save.assert_called_once_with()

        self.assertTrue(modified)
        self.assertEquals(translation.master, self.translatable)
        self.assertEquals(translation.foo, self.TRANSLATION_MSGSTR)

    def test_save_translation_without_changes(self):
        self.translatable_string.save_translation('fr')
        translation = self.translatable.get_translation('fr')
        translation.save.reset_mock()

        modified = self.translatable_string.save_translation('fr')

        translation.save.assert_not_called()
        self.assertFalse(modified)

    def test_save_translation__base_translation(self):
        with self.assertRaises(ProtectedTranslationError):
            self.translatable_string.save_translation(BASE_LANGUAGE)

        self.base_translation.save.assert_not_called()
