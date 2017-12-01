from django.test import TestCase

from django.db import models
from parler.models import TranslatableModel, TranslatedFields
from parler_po.translation_entry import TranslationEntry
import polib

class TestTranslatable(TranslatableModel):
    class Meta:
        app_label = 'parlerpo'

    translations = TranslatedFields(
        foo=models.CharField(max_length=100)
    )

class TestNotTranslatable(models.Model):
    class Meta:
        app_label = 'parlerpo'

class CreateTranslationEntryTests(TestCase):
    def test_create_with_translatable(self):
        translatable = TestTranslatable()
        translatable.id = 1
        translation_entry = TranslationEntry(translatable, 'foo', 'bar', 'baz')

        self.assertEquals(translation_entry.instance, translatable)
        self.assertEquals(translation_entry.field_id, 'foo')
        self.assertEquals(translation_entry.msgid, 'bar')
        self.assertEquals(translation_entry.msgstr, 'baz')

        self.assertEquals(translation_entry.content_type_id, 'parlerpo.testtranslatable')
        self.assertEquals(translation_entry.instance_field_id, 'parlerpo.testtranslatable@foo@1')

    def test_create_with_not_translatable(self):
        not_translatable = TestNotTranslatable()

        create_entry_fn = lambda: TranslationEntry(not_translatable, 'foo', 'bar', 'baz')
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
