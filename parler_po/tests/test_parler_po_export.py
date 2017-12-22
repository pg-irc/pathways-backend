from django.core.management import CommandError, call_command
from django.test import TestCase, override_settings

from organizations.tests.helpers import OrganizationBuilder
from parler_po.tests.helpers import add_base_translation, add_translation
from tempfile import NamedTemporaryFile, TemporaryDirectory
import io
import os
import polib

TEST_PARLER_PO_CONTACT = 'test_parler_po_export@example.com'

class ParlerPOExportCommandTests(TestCase):
    def test_requires_directory_argument(self):
        with self.assertRaisesRegex(CommandError, 'Error: the following arguments are required: directory'):
            _run_parler_po_export()

    def test_requires_a_directory_not_a_file(self):
        out_file = NamedTemporaryFile()
        with self.assertRaisesRegex(CommandError, 'Error: argument directory: The path {} must be a directory'.format(out_file.name)):
            _run_parler_po_export(out_file.name)

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

        self.out_dir = TemporaryDirectory()

    def test_exports_pot_file_for_testtranslatable(self):
        _run_parler_po_export(self.out_dir.name)

        pot_file_path = os.path.join(self.out_dir.name, 'organizations.organization.pot')
        self.assertTrue(os.path.isfile(pot_file_path))

        self._assert_po_file(
            pot_file_path,
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

    def test_exports_all_languages_for_testtranslatable(self):
        _run_parler_po_export(self.out_dir.name, all_languages=True)

        pot_file_path = os.path.join(self.out_dir.name, 'organizations.organization.pot')
        self.assertTrue(os.path.isfile(pot_file_path))

        en_po_file_path = os.path.join(self.out_dir.name, 'en', 'LC_MESSAGES', 'organizations.organization.po')
        self._assert_po_file(
            en_po_file_path,
            expected_metadata={
                'Language': 'en'
            },
            expected_po_entries=[
                polib.POEntry(
                    occurrences=[
                        ('organizations.organization@name@one', '')
                    ],
                    msgid='organization_one_translation_name_msgid',
                    msgstr='organization_one_translation_name_msgid'
                ),
                polib.POEntry(
                    occurrences=[
                        ('organizations.organization@description@two', '')
                    ],
                    msgid='organization_two_translation_description_msgid',
                    msgstr='organization_two_translation_description_msgid'
                ),
                polib.POEntry(
                    occurrences=[
                        ('organizations.organization@name@three', '')
                    ],
                    msgid='organization_three_translation_name_msgid',
                    msgstr='organization_three_translation_name_msgid'
                ),
                polib.POEntry(
                    occurrences=[
                        ('organizations.organization@description@three', '')
                    ],
                    msgid='organization_three_translation_description_msgid',
                    msgstr='organization_three_translation_description_msgid'
                )
            ]
        )

        fr_po_file_path = os.path.join(self.out_dir.name, 'fr', 'LC_MESSAGES', 'organizations.organization.po')
        self._assert_po_file(
            fr_po_file_path,
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
        _run_parler_po_export(self.out_dir.name, languages_list=['fr'])

        pot_file_path = os.path.join(self.out_dir.name, 'organizations.organization.pot')
        self.assertTrue(os.path.isfile(pot_file_path))

        en_po_file_path = os.path.join(self.out_dir.name, 'en', 'LC_MESSAGES', 'organizations.organization.po')
        self.assertFalse(os.path.isfile(en_po_file_path))

        fr_po_file_path = os.path.join(self.out_dir.name, 'fr', 'LC_MESSAGES', 'organizations.organization.po')
        self.assertTrue(os.path.isfile(fr_po_file_path))

    def _assert_po_file(self, po_file_path, expected_metadata=None, expected_po_entries=None):
        self.assertTrue(os.path.isfile(po_file_path))
        po_file = polib.pofile(po_file_path)

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
