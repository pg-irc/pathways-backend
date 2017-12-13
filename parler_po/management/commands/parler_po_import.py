from django.core.management.base import BaseCommand
from django.utils.translation import ugettext as _
import argparse
import glob
import os
import polib

from parler_po.argparse_path import argparse_path_type
from parler_po.exceptions import TranslationEntryError, ProtectedTranslationError
from parler_po.import_progress import ImportProgress
from parler_po.translation_entry import TranslationEntry

class Command(BaseCommand):
    help = _("Import the given PO files with new content translations")

    def add_arguments(self, parser):
        parser.add_argument(
            'po_paths',
            nargs='+',
            type=argparse_path_type(file_type=None, mode='w'),
            metavar='po_file'
        )

        parser.add_argument(
            '-R', '--recursive',
            dest='recursive',
            action='store_true'
        )

    def handle(self, *args, **options):
        po_paths = options['po_paths']
        recursive = options['recursive']

        for po_path in po_paths:
            if os.path.isfile(po_path):
                self._import_po_file(po_path)
            elif os.path.isdir(po_path):
                self._import_translations_dir(po_path, recursive=recursive)

    def _import_translations_dir(self, translations_dir, recursive=False):
        po_path_search = os.path.join(
            glob.escape(translations_dir), '**', '*.po'
        )
        for po_path in glob.iglob(po_path_search, recursive=recursive):
            self._import_po_file(po_path)

    def _import_po_file(self, po_path):
        self.stdout.write(
            _("Importing {file}").format(
                file=po_path
            )
        )

        po_file = polib.pofile(po_path)
        language_code = po_file.metadata.get('Language')

        if language_code:
            import_progress = ImportProgress()
            translation_entries = self._translation_entries_for_po_file(
                po_file
            )
            for translation_entry in translation_entries:
                self._import_translation_entry(
                    translation_entry, language_code, import_progress
                )
                self._print_import_progress(import_progress, ending='\r')
            self._print_import_progress(import_progress)
        else:
            self.stderr.write(
                _("Skipping \"{file}\": No language metadata").format(
                    file=po_path
                )
            )

    def _translation_entries_for_po_file(self, po_file):
        for po_entry in po_file:
            for occurrence in po_entry.occurrences:
                try:
                    translation_entry = TranslationEntry.from_po_entry(
                        po_entry, occurrence
                    )
                except TranslationEntryError as error:
                    self.stderr.write(
                        _("Skipping \"{occurrence}\": {error}").format(
                            occurrence=":".join(n for n in occurrence if n),
                            error=error
                        )
                    )
                else:
                    yield translation_entry

    def _import_translation_entry(self, translation_entry, language_code, import_progress):
        import_group = self._get_import_group(translation_entry, language_code)

        try:
            modified = translation_entry.save_translation(language_code)
        except ProtectedTranslationError as error:
            import_progress.add_skip(import_group)
        else:
            if modified:
                import_progress.add_new(import_group)
            else:
                import_progress.add_skip(import_group)

    def _print_import_progress(self, import_progress, ending='\n'):
        progress_str = str(import_progress)
        if progress_str:
            self.stderr.write(import_progress, ending=ending)

    def _get_import_group(self, translation_entry, language_code):
        return (translation_entry.model, language_code)
