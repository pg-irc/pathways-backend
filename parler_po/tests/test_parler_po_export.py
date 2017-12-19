from django.core.management import CommandError, call_command
from django.test import TestCase, override_settings
from unittest.mock import patch

from io import StringIO
from parler_po.tests.helpers import TestTranslatable
from tempfile import TemporaryDirectory
import os
import polib

TEST_PARLER_PO_CONTACT = 'test_parler_po_export@example.com'

class ParlerPOExportCommandTests(TestCase):
    def test_requires_directory_argument(self):
        with self.assertRaisesRegex(CommandError, 'Error: the following arguments are required: directory'):
            call_command('parler_po_export')

class ParlerPOExportTestsWithNoData(TestCase):
    def setUp(self):
        self.out_dir = TemporaryDirectory()

    @override_settings(PARLER_PO_CONTACT=TEST_PARLER_PO_CONTACT)
    def test_exports_empty_pot_for_testtranslatable(self):
        _run_parler_po_export_with_model(
            TestTranslatable, [], self.out_dir.name
        )

        pot_file_path = os.path.join(self.out_dir.name, 'parlerpo.testtranslatable.pot')
        self.assertTrue(os.path.isfile(pot_file_path))

        pot_file = polib.pofile(pot_file_path)
        expected_metadata = {
            'Report-Msgid-Bugs-To': TEST_PARLER_PO_CONTACT
        }
        metadata_subset = {k:v for k, v in pot_file.metadata.items() if k in expected_metadata}
        self.assertDictEqual(expected_metadata, metadata_subset)

class ParlerPOExportTestsWithBaseTranslations(TestCase):
    @override_settings(PARLER_PO_CONTACT=TEST_PARLER_PO_CONTACT)
    def setUp(self):
        self.translatable_objects = [
            TestTranslatable(id=1).with_base_translation(
                translated_field_1='translatable_1_translation_msgid_1'
            ).with_translation(
                'fr', translated_field_1='translatable_1_translation_msgstr_1'
            ),
            TestTranslatable(id=2).with_base_translation(
                translated_field_2='translatable_2_translation_msgid_2'
            ),
            TestTranslatable(id=3).with_base_translation(
                translated_field_1='translatable_3_translation_msgid_1',
                translated_field_2='translatable_3_translation_msgid_2'
            )
        ]

        self.out_dir = TemporaryDirectory()

    def test_exports_pot_file_for_testtranslatable(self):
        _run_parler_po_export_with_model(
            TestTranslatable, self.translatable_objects, self.out_dir.name
        )

        pot_file_path = os.path.join(self.out_dir.name, 'parlerpo.testtranslatable.pot')
        self.assertTrue(os.path.isfile(pot_file_path))

        pot_file = polib.pofile(pot_file_path)
        pot_entries = [n for n in pot_file]
        expected_pot_entries = [
            polib.POEntry(
                occurrences=[
                    ('parlerpo.testtranslatable@translated_field_1@1', '')
                ],
                msgid='translatable_1_translation_msgid_1',
                msgstr=''
            ),
            polib.POEntry(
                occurrences=[
                    ('parlerpo.testtranslatable@translated_field_2@2', '')
                ],
                msgid='translatable_2_translation_msgid_2',
                msgstr=''
            ),
            polib.POEntry(
                occurrences=[
                    ('parlerpo.testtranslatable@translated_field_1@3', '')
                ],
                msgid='translatable_3_translation_msgid_1',
                msgstr=''
            ),
            polib.POEntry(
                occurrences=[
                    ('parlerpo.testtranslatable@translated_field_2@3', '')
                ],
                msgid='translatable_3_translation_msgid_2',
                msgstr=''
            )
        ]

        self._assert_po_entries_equal(expected_pot_entries, pot_entries)

    def _assert_po_entries_equal(self, first, second):
        self.assertListEqual(
            list(map(_po_entry_to_dict, first)),
            list(map(_po_entry_to_dict, second))
        )

def _po_entry_to_dict(po_entry):
    return {
        'occurrences': po_entry.occurrences,
        'msgid': po_entry.msgid,
        'msgstr': po_entry.msgstr
    }

def _run_parler_po_export_with_model(model, objects, *args, **kwargs):
    with patch.object(model.objects, 'all') as model_objects_all:
        model_objects_all.return_value = objects
        with patch('parler_po.management.commands.parler_po_export.all_translatable_models') as all_translatable_models:
            all_translatable_models.return_value = [model]
            call_command('parler_po_export', *args, **kwargs)
