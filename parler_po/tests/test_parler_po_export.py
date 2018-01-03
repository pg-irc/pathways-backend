from django.core.management import CommandError, call_command
from django.test import TestCase, override_settings
from unittest.mock import call, patch

from organizations.models import Organization
from organizations.tests.helpers import OrganizationBuilder
from parler_po.tests.helpers import add_base_translation, add_translation
import io
import polib

TEST_PARLER_PO_CONTACT = 'test_parler_po_export@example.com'

class ParlerPOExportCommandTests(TestCase):
    def test_requires_model_argument(self):
        with self.assertRaisesRegex(CommandError, 'Error: one of the arguments model --list-models is required'):
            _run_parler_po_export()

class ParlerPOExportTestsWithBaseTranslations(TestCase):
    def setUp(self):
        organization_1 = OrganizationBuilder().with_id('one').build()
        add_base_translation(
            organization_1, name='organization_one_translation_name_msgid', description=''
        )
        add_translation(
            organization_1, 'fr', name='organization_one_translation_name_msgstr_fr'
        )

        organization_2 = OrganizationBuilder().with_id('two').build()
        add_base_translation(
            organization_2, name='', description='organization_two_translation_description_msgid'
        )
        add_translation(
            organization_2, 'fr', description='organization_two_translation_description_msgstr_fr'
        )

        organization_3 = OrganizationBuilder().with_id('three').build()
        add_base_translation(
            organization_3, name='organization_three_translation_name_msgid', description='organization_three_translation_description_msgid'
        )

        self.translatable_objects = [
            organization_1,
            organization_2,
            organization_3
        ]

    def test_lists_translatable_models(self):
        with patch('parler_po.management.commands.parler_po_export.all_translatable_models') as all_translatable_models:
            all_translatable_models.return_value = [Organization]
            stdout, stderr = _run_parler_po_export('--list-models')
            self.assertEqual(stdout.getvalue(), 'organizations.organization\n')

    def test_exports_pot_file_for_testtranslatable(self):
        out_file = io.StringIO()
        _run_parler_po_export('organizations.organization', file=out_file, language=None)

        self._assert_po_data(
            out_file.getvalue(),
            expected_metadata={
                'Report-Msgid-Bugs-To': TEST_PARLER_PO_CONTACT
            },
            expected_po_entries=[
                polib.POEntry(
                    occurrences=[
                        ('organizations.organization@name@one', '')
                    ],
                    msgid='organization_one_translation_name_msgid',
                    msgstr=''
                ),
                polib.POEntry(
                    occurrences=[
                        ('organizations.organization@description@two', '')
                    ],
                    msgid='organization_two_translation_description_msgid',
                    msgstr=''
                ),
                polib.POEntry(
                    occurrences=[
                        ('organizations.organization@name@three', '')
                    ],
                    msgid='organization_three_translation_name_msgid',
                    msgstr=''
                ),
                polib.POEntry(
                    occurrences=[
                        ('organizations.organization@description@three', '')
                    ],
                    msgid='organization_three_translation_description_msgid',
                    msgstr=''
                )
            ]
        )

    def test_exports_single_language_for_testtranslatable(self):
        out_file = io.StringIO()
        _run_parler_po_export('organizations.organization', file=out_file, language='fr')

        self._assert_po_data(
            out_file.getvalue(),
            expected_metadata={
                'Language': 'fr'
            },
            expected_po_entries=[
                polib.POEntry(
                    occurrences=[
                        ('organizations.organization@name@one', '')
                    ],
                    msgid='organization_one_translation_name_msgid',
                    msgstr='organization_one_translation_name_msgstr_fr'
                ),
                polib.POEntry(
                    occurrences=[
                        ('organizations.organization@description@two', '')
                    ],
                    msgid='organization_two_translation_description_msgid',
                    msgstr='organization_two_translation_description_msgstr_fr'
                )
            ]
        )

    def _assert_po_data(self, po_data, expected_metadata=None, expected_po_entries=None):
        po_file = polib.pofile(po_data)

        if expected_metadata:
            metadata_subset = {k:v for k, v in po_file.metadata.items() if k in expected_metadata}
            self.assertDictEqual(expected_metadata, metadata_subset)

        if expected_po_entries:
            po_entries_list = [n for n in po_file]
            self._assert_po_entries_equal(po_entries_list, expected_po_entries)

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

@override_settings(PARLER_PO_CONTACT=TEST_PARLER_PO_CONTACT)
def _run_parler_po_export(*args, **kwargs):
    stdout = io.StringIO()
    stderr = io.StringIO()
    call_command('parler_po_export', *args, **kwargs, stdout=stdout, stderr=stderr)
    return stdout, stderr
