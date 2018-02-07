from django.test import TestCase
from unittest.mock import call, patch

from translation.exceptions import (
    FieldNotTranslatableError,
    InvalidMsgidError,
    MasterInstanceLookupError,
    MissingMsgidError,
    ModelNotTranslatableError,
    ProtectedTranslationError
)
from human_services.organizations.tests.helpers import OrganizationBuilder
from translation.tests.helpers import add_base_translation, add_translation
from translation.tests.models import TestNotTranslatable
from translation.translatable_string import TranslatableString
import polib

class CreateTranslatableStringTests(TestCase):
    def test_create_with_translatable_model(self):
        translatable = OrganizationBuilder().with_id('test_create_with_translatable_model_id').build()

        add_base_translation(
            translatable, name='translation_name_msgid'
        )

        translatable_string = TranslatableString(translatable, 'name', 'translation_name_msgid', 'translation_name_msgstr')

        self.assertEqual(translatable_string._instance, translatable)
        self.assertEqual(translatable_string._field_id, 'name')
        self.assertEqual(translatable_string._source_str, 'translation_name_msgid')
        self.assertEqual(translatable_string._translated_str, 'translation_name_msgstr')

        self.assertEqual(str(translatable_string), 'organizations.organization@name@test_create_with_translatable_model_id')

    def test_create_with_not_translatable_model_raises_error(self):
        not_translatable = TestNotTranslatable()

        with self.assertRaises(ModelNotTranslatableError):
            TranslatableString(not_translatable, 'name', 'translation_name_msgid', 'translation_name_msgstr')

    def test_create_with_not_translatable_field_raises_error(self):
        translatable = OrganizationBuilder().build()

        with self.assertRaises(FieldNotTranslatableError):
            TranslatableString(translatable, 'static', 'translation_name_msgid', 'translation_name_msgstr')

    def test_create_with_invalid_field_raises_error(self):
        translatable = OrganizationBuilder().build()

        with self.assertRaises(FieldNotTranslatableError):
            TranslatableString(translatable, 'not_a_field', 'translation_name_msgid', 'translation_name_msgstr')

    def test_create_without_msgid_raises_error(self):
        translatable = OrganizationBuilder().with_id('test_create_without_msgid_raises_error_id').with_name('').build()

        with self.assertRaises(MissingMsgidError):
            TranslatableString(translatable, 'name', '', 'translation_name_msgstr')

    def test_create_with_different_msgid_from_base_translation_raises_error(self):
        translatable = OrganizationBuilder().with_id('test_create_with_different_msgid_from_base_translation_raises_error_id').with_name('translated_name_msgid').build()

        with self.assertRaises(InvalidMsgidError):
            TranslatableString(translatable, 'name', 'not_translation_name_msgid', 'translation_name_msgstr')

    def test_create_from_po_entry(self):
        translatable = OrganizationBuilder().with_id('test_create_from_po_entry_id').build()

        base_translation = add_base_translation(
            translatable, name='translation_name_msgid'
        )

        po_entry = polib.POEntry()
        po_entry.occurrences = [
            ('organizations.organization@name@test_create_from_po_entry', None)
        ]
        po_entry.msgid = 'translation_name_msgid'
        po_entry.msgstr = 'translation_name_msgstr'

        with patch('translation.translatable_string.parse_instance_field_id') as parse_instance_field_id:
            parse_instance_field_id.return_value = (translatable, 'name')
            translatable_string = TranslatableString.from_po_entry(po_entry, po_entry.occurrences[0])
            parse_instance_field_id.assert_called_once_with('organizations.organization@name@test_create_from_po_entry')

        self.assertEqual(translatable_string._instance, translatable)
        self.assertEqual(translatable_string._field_id, 'name')
        self.assertEqual(translatable_string._source_str, 'translation_name_msgid')
        self.assertEqual(translatable_string._translated_str, 'translation_name_msgstr')

    def test_create_from_po_entry_with_invalid_occurrence_format_raise_error(self):
        translatable = OrganizationBuilder().with_id('test_create_from_po_entry_with_invalid_occurrence_format_raise_error_id').build()

        po_entry = polib.POEntry()
        po_entry.occurrences = [
            ('bad format', None)
        ]
        po_entry.msgid = 'translation_name_msgid'
        po_entry.msgstr = 'translation_name_msgstr'

        with self.assertRaises(MasterInstanceLookupError):
            TranslatableString.from_po_entry(po_entry, po_entry.occurrences[0])

    def test_create_from_po_entry_with_nonexistent_master_instance_raises_error(self):
        translatable = OrganizationBuilder().with_id('test_create_from_po_entry_with_nonexistent_master_instance_raises_error_id').build()

        po_entry = polib.POEntry()
        po_entry.occurrences = [
            ('organizations.organization@name@not_an_id', None)
        ]
        po_entry.msgid = 'translation_name_msgid'
        po_entry.msgstr = 'translation_name_msgstr'

        with self.assertRaises(MasterInstanceLookupError):
            TranslatableString.from_po_entry(po_entry, po_entry.occurrences[0])

    def test_create_from_po_entry_with_not_translatable_master_instance_raises_error(self):
        translatable = TestNotTranslatable(id='test_create_from_po_entry_with_not_translatable_master_instance_raises_error_id')

        po_entry = polib.POEntry()
        po_entry.occurrences = [
            ('contenttranslationtools.testnottranslatable@name@test_create_from_po_entry_with_not_translatable_master_instance_raises_error_id', None)
        ]
        po_entry.msgid = 'translation_name_msgid'
        po_entry.msgstr = 'translation_name_msgstr'

        with patch('translation.translatable_string.parse_instance_field_id') as parse_instance_field_id:
            parse_instance_field_id.return_value = (translatable, 'name')
            with self.assertRaises(ModelNotTranslatableError):
                TranslatableString.from_po_entry(po_entry, po_entry.occurrences[0])

    def test_all_from_po_entry(self):
        translatable = OrganizationBuilder().with_id('test_all_from_po_entry_id').build()

        base_translation = add_base_translation(
            translatable, name='translation_name_msgid'
        )

        po_entry = polib.POEntry()
        po_entry.occurrences = [
            ('organizations.organization@name@test_all_from_po_entry_id', None)
        ]
        po_entry.msgid = 'translation_name_msgid'
        po_entry.msgstr = 'translation_name_msgstr'

        with patch.object(TranslatableString, 'from_po_entry') as from_po_entry:
            errors_list = []
            results_iter = TranslatableString.all_from_po_entry(po_entry, errors_out=errors_list)
            results_list = [n for n in results_iter]
            self.assertEqual(from_po_entry.call_count, 1)
            from_po_entry.assert_has_calls([
                call(po_entry, po_entry.occurrences[0])
            ])

        self.assertEqual(len(errors_list), 0)
        self.assertEqual(len(results_list), 1)

    def test_create_from_translation(self):
        translatable = OrganizationBuilder().with_id('test_create_from_translation_id').build()

        base_translation = add_base_translation(
            translatable, name='translation_name_msgid'
        )
        translation = add_translation(
            translatable, 'fr', name='translation_name_msgstr'
        )

        translatable_string = TranslatableString.from_translation(translation, 'name')

        self.assertEqual(translatable_string._instance, translatable)
        self.assertEqual(translatable_string._field_id, 'name')
        self.assertEqual(translatable_string._source_str, 'translation_name_msgid')
        self.assertEqual(translatable_string._translated_str, 'translation_name_msgstr')

    def test_create_from_translation_with_missing_msgid_raises_error(self):
        translatable = OrganizationBuilder().with_id('test_create_from_translation_with_missing_msgid_raises_error_id').build()

        base_translation = add_base_translation(
            translatable, name=''
        )
        translation = add_translation(
            translatable, 'fr', name='translation_name_msgstr'
        )

        with self.assertRaises(MissingMsgidError):
            TranslatableString.from_translation(translation, 'name')

    def test_all_from_translation(self):
        translatable = OrganizationBuilder().with_id('test_all_from_translation_id').build()

        base_translation = add_base_translation(
            translatable, name='translation_name_msgid', description='translation_description_msgid'
        )
        translation = add_translation(
            translatable, 'fr', name='translation_name_msgstr'
        )

        with patch.object(TranslatableString, 'from_translation') as from_translation:
            errors_list = []
            results_iter = TranslatableString.all_from_translation(translation, errors_out=errors_list)
            results_list = [n for n in results_iter]
            self.assertEqual(from_translation.call_count, 2)
            from_translation.assert_has_calls([
                call(translation, 'name'),
                call(translation, 'description')
            ])

        self.assertEqual(len(errors_list), 0)
        self.assertEqual(len(results_list), 2)


class ValidTranslatableStringTests(TestCase):
    def setUp(self):
        self.translatable = OrganizationBuilder().with_id('translatable_string_tests_id').build()

        self.base_translation = add_base_translation(
            self.translatable, name='translation_name_msgid'
        )

        if self.translatable.has_translation('fr'):
            self.translatable.delete_translation('fr')

        self.translatable_string = TranslatableString(
            self.translatable, 'name', 'translation_name_msgid', 'translation_name_msgstr'
        )

    def test_as_po_entry(self):
        po_entry = self.translatable_string.as_po_entry()

        self.assertEqual(po_entry.msgid, 'translation_name_msgid')
        self.assertEqual(po_entry.msgstr, 'translation_name_msgstr')
        self.assertEqual(po_entry.occurrences, [
            ('organizations.organization@{}@{}'.format('name', 'translatable_string_tests_id'), None)
        ])

    def test_save_translation_returns_true_if_created(self):
        modified = self.translatable_string.save_translation('fr')
        self.assertTrue(modified)

        translation = self.translatable.get_translation('fr')
        self.assertTrue(modified)
        self.assertEqual(translation.master, self.translatable)
        self.assertEqual(translation.name, 'translation_name_msgstr')

    def test_save_translation_returns_false_if_unchanged(self):
        self.translatable_string.save_translation('fr')
        modified = self.translatable_string.save_translation('fr')
        self.assertFalse(modified)

    def test_save_translation_returns_true_if_modified(self):
        new_translatable_string = TranslatableString(
            self.translatable, 'name', 'translation_name_msgid', 'translation_name_msgstr_2'
        )

        self.translatable_string.save_translation('fr')
        modified = new_translatable_string.save_translation('fr')
        self.assertTrue(modified)

    def test_save_translation_creates_translation(self):
        self.translatable_string.save_translation('fr')

        translation = self.translatable.get_translation('fr')
        self.assertEqual(translation.master, self.translatable)
        self.assertEqual(translation.name, 'translation_name_msgstr')

    def test_save_translation_changes_fields_if_modified(self):
        new_translatable_string = TranslatableString(
            self.translatable, 'name', 'translation_name_msgid', 'translation_name_msgstr_2'
        )

        self.translatable_string.save_translation('fr')
        new_translatable_string.save_translation('fr')

        translation = self.translatable.get_translation('fr')
        self.assertEqual(translation.master, self.translatable)
        self.assertEqual(translation.name, 'translation_name_msgstr_2')

    def test_save_translation_with_base_translation_raises_error(self):
        base_language = self.base_translation.language_code
        with self.assertRaises(ProtectedTranslationError):
            self.translatable_string.save_translation(base_language)
