from django.test import TestCase
from unittest.mock import call, patch

from parler_po.exceptions import (
    FieldNotTranslatableError,
    InvalidMsgidError,
    MasterInstanceLookupError,
    MissingMsgidError,
    ModelNotTranslatableError,
    ProtectedTranslationError
)
from parler_po.tests.helpers import TestTranslatable, TestNotTranslatable
from parler_po.translatable_string import TranslatableString
import polib

class CreateTranslatableStringTests(TestCase):
    def test_create_with_translatable_model(self):
        translatable = TestTranslatable(id=1).with_base_translation(
            translated_field_1='translation_msgid_1'
        )

        translatable_string = TranslatableString(translatable, 'translated_field_1', 'translation_msgid_1', 'translation_msgstr_1')

        self.assertEquals(translatable_string._instance, translatable)
        self.assertEquals(translatable_string._field_id, 'translated_field_1')
        self.assertEquals(translatable_string._source_str, 'translation_msgid_1')
        self.assertEquals(translatable_string._translated_str, 'translation_msgstr_1')

        self.assertEquals(str(translatable_string), 'parlerpo.testtranslatable@translated_field_1@1')

    def test_create_with_not_translatable_model_raises_error(self):
        not_translatable = TestNotTranslatable()

        with self.assertRaises(ModelNotTranslatableError):
            TranslatableString(not_translatable, 'translated_field_1', 'translation_msgid_1', 'translation_msgstr_1')

    def test_create_with_not_translatable_field_raises_error(self):
        translatable = TestTranslatable()

        with self.assertRaises(FieldNotTranslatableError):
            TranslatableString(translatable, 'static', 'translation_msgid_1', 'translation_msgstr_1')

    def test_create_with_invalid_field_raises_error(self):
        translatable = TestTranslatable()

        with self.assertRaises(FieldNotTranslatableError):
            TranslatableString(translatable, 'not_a_field', 'translation_msgid_1', 'translation_msgstr_1')

    def test_create_without_msgid_raises_error(self):
        translatable = TestTranslatable(id=1, translated_field_1='')

        with self.assertRaises(MissingMsgidError):
            TranslatableString(translatable, 'translated_field_1', '', 'translation_msgstr_1')

    def test_create_with_different_msgid_from_base_translation_raises_error(self):
        translatable = TestTranslatable(id=1, translated_field_1='translated_msgid_1')

        with self.assertRaises(InvalidMsgidError):
            TranslatableString(translatable, 'translated_field_1', 'not_translation_msgid_1', 'translation_msgstr_1')

    def test_create_from_po_entry(self):
        translatable = TestTranslatable(id=1).with_base_translation(
            translated_field_1='translation_msgid_1'
        )

        po_entry = polib.POEntry()
        po_entry.occurrences = [
            ('parlerpo.testtranslatable@translated_field_1@1', None)
        ]
        po_entry.msgid = 'translation_msgid_1'
        po_entry.msgstr = 'translation_msgstr_1'

        with patch('parler_po.translatable_string.parse_instance_field_id') as parse_instance_field_id:
            parse_instance_field_id.return_value = (translatable, 'translated_field_1')
            translatable_string = TranslatableString.from_po_entry(po_entry, po_entry.occurrences[0])
            parse_instance_field_id.assert_called_once_with('parlerpo.testtranslatable@translated_field_1@1')

        self.assertEquals(translatable_string._instance, translatable)
        self.assertEquals(translatable_string._field_id, 'translated_field_1')
        self.assertEquals(translatable_string._source_str, 'translation_msgid_1')
        self.assertEquals(translatable_string._translated_str, 'translation_msgstr_1')

    def test_create_from_po_entry_with_invalid_occurrence_format_raise_error(self):
        translatable = TestTranslatable(id=1)

        po_entry = polib.POEntry()
        po_entry.occurrences = [
            ('bad format', None)
        ]
        po_entry.msgid = 'translation_msgid_1'
        po_entry.msgstr = 'translation_msgstr_1'

        with self.assertRaises(MasterInstanceLookupError):
            TranslatableString.from_po_entry(po_entry, po_entry.occurrences[0])

    def test_create_from_po_entry_with_nonexistent_master_instance_raises_error(self):
        translatable = TestTranslatable(id=1)

        po_entry = polib.POEntry()
        po_entry.occurrences = [
            ('parlerpo.testtranslatable@translated_field_1@1000', None)
        ]
        po_entry.msgid = 'translation_msgid_1'
        po_entry.msgstr = 'translation_msgstr_1'

        with self.assertRaises(MasterInstanceLookupError):
            TranslatableString.from_po_entry(po_entry, po_entry.occurrences[0])

    def test_create_from_po_entry_with_not_translatable_master_instance_raises_error(self):
        translatable = TestNotTranslatable(id=1)

        po_entry = polib.POEntry()
        po_entry.occurrences = [
            ('parlerpo.testnottranslatable@translated_field_1@1', None)
        ]
        po_entry.msgid = 'translation_msgid_1'
        po_entry.msgstr = 'translation_msgstr_1'

        with patch('parler_po.translatable_string.parse_instance_field_id') as parse_instance_field_id:
            parse_instance_field_id.return_value = (translatable, 'translated_field_1')
            with self.assertRaises(ModelNotTranslatableError):
                TranslatableString.from_po_entry(po_entry, po_entry.occurrences[0])

    def test_all_from_po_entry(self):
        translatable = TestTranslatable(id=1).with_base_translation(
            translated_field_1='translation_msgid_1'
        )

        po_entry = polib.POEntry()
        po_entry.occurrences = [
            ('parlerpo.testtranslatable@translated_field_1@1', None)
        ]
        po_entry.msgid = 'translation_msgid_1'
        po_entry.msgstr = 'translation_msgstr_1'

        with patch.object(TranslatableString, 'from_po_entry') as from_po_entry:
            errors_list = []
            results_iter = TranslatableString.all_from_po_entry(po_entry, errors_out=errors_list)
            results_list = [n for n in results_iter]
            self.assertEquals(from_po_entry.call_count, 1)
            from_po_entry.assert_has_calls([
                call(po_entry, po_entry.occurrences[0])
            ])

        self.assertEqual(len(errors_list), 0)
        self.assertEqual(len(results_list), 1)

    def test_create_from_translation(self):
        translatable = TestTranslatable(id=1).with_base_translation(
            translated_field_1='translation_msgid_1'
        ).with_translation(
            'fr', translated_field_1='translation_msgstr_1'
        )

        translation = translatable.get_translation('fr')
        translatable_string = TranslatableString.from_translation(translation, 'translated_field_1')

        self.assertEquals(translatable_string._instance, translatable)
        self.assertEquals(translatable_string._field_id, 'translated_field_1')
        self.assertEquals(translatable_string._source_str, 'translation_msgid_1')
        self.assertEquals(translatable_string._translated_str, 'translation_msgstr_1')

    def test_create_from_translation_with_missing_msgid_raises_error(self):
        translatable = TestTranslatable(id=1).with_base_translation(
            translated_field_1=''
        ).with_translation(
            'fr', translated_field_1='translation_msgstr_1'
        )

        translation = translatable.get_translation('fr')

        with self.assertRaises(MissingMsgidError):
            TranslatableString.from_translation(translation, 'translated_field_1')

    def test_all_from_translation(self):
        translatable = TestTranslatable(id=1).with_base_translation(
            translated_field_1='translation_msgid_1',
            translated_field_2='translation_msgid_2',
            translated_field_3='translation_msgid_3'
        ).with_translation(
            'fr', translated_field_1='translation_msgstr_1'
        )

        translation = translatable.get_translation('fr')

        with patch.object(TranslatableString, 'from_translation') as from_translation:
            errors_list = []
            results_iter = TranslatableString.all_from_translation(translation, errors_out=errors_list)
            results_list = [n for n in results_iter]
            self.assertEquals(from_translation.call_count, 3)
            from_translation.assert_has_calls([
                call(translation, 'translated_field_1'),
                call(translation, 'translated_field_2'),
                call(translation, 'translated_field_3')
            ])

        self.assertEqual(len(errors_list), 0)
        self.assertEqual(len(results_list), 3)


class ValidTranslatableStringTests(TestCase):
    def setUp(self):
        self.translatable = TestTranslatable(id=1).with_base_translation(
            translated_field_1='translation_msgid_1'
        )
        self.base_translation = self.translatable.get_base_translation()
        self.translatable_string = TranslatableString(
            self.translatable, 'translated_field_1', 'translation_msgid_1', 'translation_msgstr_1'
        )

    def test_as_po_entry(self):
        po_entry = self.translatable_string.as_po_entry()

        self.assertEquals(po_entry.msgid, 'translation_msgid_1')
        self.assertEquals(po_entry.msgstr, 'translation_msgstr_1')
        self.assertEquals(po_entry.occurrences, [
            ('parlerpo.testtranslatable@{}@{}'.format('translated_field_1', 1), None)
        ])

    def test_save_new_translation(self):
        modified = self.translatable_string.save_translation('fr')
        translation = self.translatable.get_translation('fr')

        translation.save.assert_called_once_with()

        self.assertTrue(modified)
        self.assertEquals(translation.master, self.translatable)
        self.assertEquals(translation.translated_field_1, 'translation_msgstr_1')

    def test_save_translation_without_changes_returns_false(self):
        self.translatable_string.save_translation('fr')
        translation = self.translatable.get_translation('fr')
        translation.save.reset_mock()

        modified = self.translatable_string.save_translation('fr')

        translation.save.assert_not_called()
        self.assertFalse(modified)

    def test_save_translation_with_base_translation_raises_error(self):
        base_language = self.base_translation.language_code

        self.assertEquals(base_language, 'en')

        with self.assertRaises(ProtectedTranslationError):
            self.translatable_string.save_translation(base_language)

        self.base_translation.save.assert_not_called()
