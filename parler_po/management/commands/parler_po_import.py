from django.core.management.base import BaseCommand
from django.utils.translation import ugettext as _
import argparse
import glob
import os
import polib

from parler_po.argparse_path import argparse_path_type
from parler_po.exceptions import ParlerPOError, ProtectedTranslationError
from parler_po.import_progress import ImportProgress
from parler_po.translatable_string import TranslatableString

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
            _("{file}:").format(
                file=po_path
            )
        )

        po_file = polib.pofile(po_path)
        language_code = po_file.metadata.get('Language')

        if language_code:
            import_progress = ImportProgress()
            translatable_strings = self._translatable_strings_for_po_file(
                po_file
            )
            for translatable_string in translatable_strings:
                self._import_translatable_string(
                    translatable_string, language_code, import_progress
                )
                self._print_import_progress(import_progress, ending='\r')
            self._print_import_progress(import_progress)
        else:
            self.stderr.write(
                _("Skipping \"{file}\": No language metadata").format(
                    file=po_path
                )
            )

    def _translatable_strings_for_po_file(self, po_file):
        errors_list = []

        for po_entry in po_file:
            yield from TranslatableString.all_from_po_entry(
                po_entry, errors_out=errors_list
            )

        for error in errors_list:
            self.stderr.write(error)

    def _import_translatable_string(self, translatable_string, language_code, import_progress):
        import_group = self._get_import_group(translatable_string, language_code)

        try:
            modified = translatable_string.save_translation(language_code)
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
            self.stderr.write(progress_str, ending=ending)

    def _get_import_group(self, translatable_string, language_code):
        return (translatable_string.model, language_code)
