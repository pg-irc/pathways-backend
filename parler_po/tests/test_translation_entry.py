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

    def get_translation(language_code):
        return self.translations.model(
            master=self,
            language_code=language_code
        )

class TestNotTranslatable(models.Model):
    class Meta:
        app_label = 'parlerpo'
        managed = False

class CreateTranslationEntryTests(TestCase):
    def test_create_with_translatable(self):
        translatable = TestTranslatable()
        translatable.id = 1
        translation_entry = TranslationEntry(translatable, 'foo', 'bar', 'baz')

        self.assertEquals(translation_entry.instance, translatable)
        self.assertEquals(translation_entry.field_id, 'foo')
        self.assertEquals(translation_entry.msgid, 'bar')
        self.assertEquals(translation_entry.msgstr, 'baz')

        self.assertEquals(str(translation_entry), 'parlerpo.testtranslatable@foo@1')

    def test_create_not_translatable(self):
        not_translatable = TestNotTranslatable()

        create_entry_fn = lambda: TranslationEntry(not_translatable, 'foo', 'bar', 'baz')
        self.assertRaises(TypeError, create_entry_fn)

    def test_create_with_static_field(self):
        translatable = TestTranslatable()

        create_entry_fn = lambda: TranslationEntry(translatable, 'static', 'bar', 'baz')
        self.assertRaises(ValueError, create_entry_fn)

    def test_create_with_invalid_field(self):
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

    def test_create_not_translatable_from_po_entry(self):
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

class ValidTranslationEntryTests(TestCase):
    TRANSLATION_FIELD = 'foo'
    TRANSLATION_MSGID = 'bar'
    TRANSLATION_MSGSTR = 'baz'
    TRANSLATABLE_ID = 1

    def setUp(self):
        translatable = TestTranslatable()
        translatable.id = self.TRANSLATABLE_ID
        translatable.foo = self.TRANSLATION_MSGID
        self.translation_entry = TranslationEntry(
            translatable, self.TRANSLATION_FIELD, self.TRANSLATION_MSGID, self.TRANSLATION_MSGSTR
        )

    def test_as_po_entry(self):
        po_entry = self.translation_entry.as_po_entry()

        self.assertEquals(po_entry.msgid, self.TRANSLATION_MSGID)
        self.assertEquals(po_entry.msgstr, self.TRANSLATION_MSGSTR)
        self.assertEquals(po_entry.occurrences, [
            ('parlerpo.testtranslatable@{}@{}'.format(self.TRANSLATION_FIELD, self.TRANSLATABLE_ID), None)
        ])
