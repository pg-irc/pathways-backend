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
from parler_po.translation_entry import TranslationEntry
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

    _TRANSLATIONS_DICT = {}

    def get_translation(self, language_code):
        translation = self._TRANSLATIONS_DICT.get(language_code)

        if not translation:
            translation = MagicMock()
            translation.master = self
            translation.language_code = language_code
            self._TRANSLATIONS_DICT[language_code] = translation

        return translation

    def create_translation(self, language_code):
        self.get_translation(language_code)

    def has_translation(self, language_code):
        return language_code in self._TRANSLATIONS_DICT

class TestNotTranslatable(models.Model):
    class Meta:
        app_label = 'parlerpo'
        managed = False

class CreateTranslationEntryTests(TestCase):
    def test_create__translatable(self):
        translatable = TestTranslatable()
        translatable.id = 1

        base_translation = translatable.get_translation('en')
        base_translation.foo = 'bar'

        translation_entry = TranslationEntry(translatable, 'foo', 'bar', 'baz')

        self.assertEquals(translation_entry._instance, translatable)
        self.assertEquals(translation_entry._field_id, 'foo')
        self.assertEquals(translation_entry._msgid, 'bar')
        self.assertEquals(translation_entry._msgstr, 'baz')

        self.assertEquals(str(translation_entry), 'parlerpo.testtranslatable@foo@1')

    def test_create__not_translatable(self):
        not_translatable = TestNotTranslatable()

        with self.assertRaises(ModelNotTranslatableError):
            TranslationEntry(not_translatable, 'foo', 'bar', 'baz')

    def test_create__static_field(self):
        translatable = TestTranslatable()

        with self.assertRaises(FieldNotTranslatableError):
            TranslationEntry(translatable, 'static', 'bar', 'baz')

    def test_create__invalid_field(self):
        translatable = TestTranslatable()

        with self.assertRaises(FieldNotTranslatableError):
            TranslationEntry(translatable, 'not_a_field', 'bar', 'baz')

    def test_create__invalid_msgid(self):
        translatable = TestTranslatable()
        translatable.id = 1
        translatable.foo = 'not_bar'

        with self.assertRaises(InvalidMsgidError):
            TranslationEntry(translatable, 'foo', 'bar', 'baz')

    def test_create__missing_msgid(self):
        translatable = TestTranslatable()
        translatable.id = 1
        translatable.foo = ''

        with self.assertRaises(MissingMsgidError):
            TranslationEntry(translatable, 'foo', '', 'baz')

    def test_create_from_po_entry(self):
        translatable = TestTranslatable()
        translatable.id = 1

        po_entry = polib.POEntry()
        po_entry.occurrences = [
            ('parlerpo.testtranslatable@foo@1', None)
        ]
        po_entry.msgid = 'bar'
        po_entry.msgstr = 'baz'

        with patch('parler_po.translation_entry.parse_instance_field_id') as parse_instance_field_id:
            parse_instance_field_id.return_value = (translatable, 'foo')
            translation_entry = TranslationEntry.from_po_entry(po_entry, po_entry.occurrences[0])
            parse_instance_field_id.assert_called_once_with('parlerpo.testtranslatable@foo@1')

        self.assertEquals(translation_entry._instance, translatable)
        self.assertEquals(translation_entry._field_id, 'foo')
        self.assertEquals(translation_entry._msgid, 'bar')
        self.assertEquals(translation_entry._msgstr, 'baz')

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
            TranslationEntry.from_po_entry(po_entry, po_entry.occurrences[0])

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
            TranslationEntry.from_po_entry(po_entry, po_entry.occurrences[0])

    def test_create_from_po_entry__not_translatable(self):
        translatable = TestNotTranslatable()
        translatable.id = 1

        po_entry = polib.POEntry()
        po_entry.occurrences = [
            ('parlerpo.testnottranslatable@foo@1', None)
        ]
        po_entry.msgid = 'bar'
        po_entry.msgstr = 'baz'

        with patch('parler_po.translation_entry.parse_instance_field_id') as parse_instance_field_id:
            parse_instance_field_id.return_value = (translatable, 'foo')
            with self.assertRaises(ModelNotTranslatableError):
                TranslationEntry.from_po_entry(po_entry, po_entry.occurrences[0])

    def test_create_from_translation(self):
        translatable = TestTranslatable()
        translatable.id = 1

        base_translation = translatable.get_translation(BASE_LANGUAGE)
        base_translation.foo = 'bar'

        translation = translatable.get_translation('fr')
        translation.foo = 'baz'

        translation_entry = TranslationEntry.from_translation(translation, 'foo')

        self.assertEquals(translation_entry._instance, translatable)
        self.assertEquals(translation_entry._field_id, 'foo')
        self.assertEquals(translation_entry._msgid, 'bar')
        self.assertEquals(translation_entry._msgstr, 'baz')

    def test_create_from_translation__missing_msgid(self):
        translatable = TestTranslatable()
        translatable.id = 1

        base_translation = translatable.get_translation(BASE_LANGUAGE)
        base_translation.foo = ''

        translation = translatable.get_translation('fr')
        translation.foo = 'baz'

        with self.assertRaises(MissingMsgidError):
            TranslationEntry.from_translation(translation, 'foo')

class ValidTranslationEntryTests(TestCase):
    TRANSLATION_FIELD = 'foo'
    TRANSLATION_MSGID = 'bar'
    TRANSLATION_MSGSTR = 'baz'
    TRANSLATABLE_ID = 1

    def setUp(self):
        self.translatable = TestTranslatable()
        self.translatable.id = self.TRANSLATABLE_ID

        self.base_translation = self.translatable.get_translation(BASE_LANGUAGE)
        self.base_translation.foo = self.TRANSLATION_MSGID

        self.translation_entry = TranslationEntry(
            self.translatable, self.TRANSLATION_FIELD, self.TRANSLATION_MSGID, self.TRANSLATION_MSGSTR
        )

    def test_as_po_entry(self):
        po_entry = self.translation_entry.as_po_entry()

        self.assertEquals(po_entry.msgid, self.TRANSLATION_MSGID)
        self.assertEquals(po_entry.msgstr, self.TRANSLATION_MSGSTR)
        self.assertEquals(po_entry.occurrences, [
            ('parlerpo.testtranslatable@{}@{}'.format(self.TRANSLATION_FIELD, self.TRANSLATABLE_ID), None)
        ])

    def test_save_translation(self):
        modified = self.translation_entry.save_translation('fr')
        translation = self.translatable.get_translation('fr')

        self.assertTrue(modified)
        self.assertEquals(translation.master, self.translatable)
        self.assertEquals(translation.foo, self.TRANSLATION_MSGSTR)

        translation.save.assert_called_once_with()

    def test_save_translation__base_translation(self):
        with self.assertRaises(ProtectedTranslationError):
            self.translation_entry.save_translation(BASE_LANGUAGE)

        self.base_translation.save.assert_not_called()
