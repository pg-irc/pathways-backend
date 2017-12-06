from django.test import TestCase
from unittest.mock import patch

from django.db import models
from parler.models import TranslatableModel, TranslatedFields
from parler_po.translation_entry import TranslationEntry
import polib

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
        return self._TRANSLATIONS_DICT.setdefault(
            language_code,
            self.translations.model(
                master=self,
                language_code=language_code
            )
        )

    def create_translation(self, language_code):
        self.get_translation(language_code)

class TestNotTranslatable(models.Model):
    class Meta:
        app_label = 'parlerpo'
        managed = False

class CreateTranslationEntryTests(TestCase):
    def test_create__translatable(self):
        translatable = TestTranslatable()
        translatable.id = 1
        translation_entry = TranslationEntry(translatable, 'foo', 'bar', 'baz')

        self.assertEquals(translation_entry.instance, translatable)
        self.assertEquals(translation_entry.field_id, 'foo')
        self.assertEquals(translation_entry.msgid, 'bar')
        self.assertEquals(translation_entry.msgstr, 'baz')

        self.assertEquals(str(translation_entry), 'parlerpo.testtranslatable@foo@1')

    def test_create__not_translatable(self):
        not_translatable = TestNotTranslatable()

        create_entry_fn = lambda: TranslationEntry(not_translatable, 'foo', 'bar', 'baz')
        self.assertRaises(TypeError, create_entry_fn)

    def test_create__static_field(self):
        translatable = TestTranslatable()

        create_entry_fn = lambda: TranslationEntry(translatable, 'static', 'bar', 'baz')
        self.assertRaises(ValueError, create_entry_fn)

    def test_create__invalid_field(self):
        translatable = TestTranslatable()

        create_entry_fn = lambda: TranslationEntry(translatable, 'not_a_field', 'bar', 'baz')
        self.assertRaises(ValueError, create_entry_fn)

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
            translation_entry = TranslationEntry.from_po_entry(
                po_entry,
                po_entry.occurrences[0]
            )
            parse_instance_field_id.assert_called_once_with('parlerpo.testtranslatable@foo@1')

        self.assertEquals(translation_entry.instance, translatable)
        self.assertEquals(translation_entry.field_id, 'foo')
        self.assertEquals(translation_entry.msgid, 'bar')
        self.assertEquals(translation_entry.msgstr, 'baz')

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
            create_entry_fn = lambda: TranslationEntry.from_po_entry(
                po_entry,
                po_entry.occurrences[0]
            )
            self.assertRaises(TypeError, create_entry_fn)

    def test_create_from_translation(self):
        translatable = TestTranslatable()
        translatable.id = 1

        base_translation = translatable.get_translation('en')
        base_translation.foo = 'bar'

        translation = translatable.get_translation('fr')
        translation.foo = 'baz'

        translation_entry = TranslationEntry.from_translation(translation, 'foo')

        self.assertEquals(translation_entry.instance, translatable)
        self.assertEquals(translation_entry.field_id, 'foo')
        self.assertEquals(translation_entry.msgid, 'bar')
        self.assertEquals(translation_entry.msgstr, 'baz')

class ValidTranslationEntryTests(TestCase):
    TRANSLATION_FIELD = 'foo'
    TRANSLATION_MSGID = 'bar'
    TRANSLATION_MSGSTR = 'baz'
    TRANSLATABLE_ID = 1

    def setUp(self):
        self.translatable = TestTranslatable()
        self.translatable.id = self.TRANSLATABLE_ID
        self.translatable.foo = self.TRANSLATION_MSGID
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

    def test_as_po_entry__no_msgid(self):
        self.translation_entry.msgid = ''

        as_translation_fn = lambda: self.translation_entry.as_po_entry()

        self.assertRaises(ValueError, as_translation_fn)

    def test_as_translation(self):
        translation = self.translation_entry.as_translation('fr')

        self.assertEquals(translation.master, self.translatable)
        self.assertEquals(translation.foo, self.TRANSLATION_MSGSTR)
        self.assertTrue(translation.is_modified)

    def test_as_translation__base_translation(self):
        translation = self.translation_entry.as_translation('en')

        self.assertIsNone(translation)

    def test_as_translation__invalid_msgid(self):
        self.translation_entry.msgid = 'not_bar'

        as_translation_fn = lambda: self.translation_entry.as_translation('fr')

        self.assertRaises(ValueError, as_translation_fn)
