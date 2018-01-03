from django.core.management.base import BaseCommand
from django.utils.translation import ugettext as _
import argparse
import polib
import sys

from content_translation_tools.exceptions import ProtectedTranslationError
from content_translation_tools.import_progress import ImportProgress
from content_translation_tools.translatable_string import TranslatableString

class Command(BaseCommand):
    help = _('Import a PO file with new content translations')

    def add_arguments(self, parser):
        parser.add_argument(
            'file',
            type=argparse.FileType('r'),
            default=sys.stdin
        )

    def handle(self, *args, **options):
        in_file = options['file']

        self._import_po_file(in_file)

    def _import_po_file(self, in_file):
        po_file = polib.pofile(in_file.read())

        language = po_file.metadata.get('Language')

        if language:
            import_progress = ImportProgress()
            translatable_strings = self._translatable_strings_for_po_file(
                po_file
            )
            for translatable_string in translatable_strings:
                self._import_translatable_string(
                    translatable_string, language, import_progress
                )
                self._print_import_progress(import_progress, ending='\r')
            self._print_import_progress(import_progress)
        else:
            self.stderr.write(
                _('Skipping file: No language metadata')
            )

    def _translatable_strings_for_po_file(self, po_file):
        errors_list = []

        for po_entry in po_file:
            yield from TranslatableString.all_from_po_entry(
                po_entry, errors_out=errors_list
            )

        for error in errors_list:
            self.stderr.write(error)

    def _import_translatable_string(self, translatable_string, language, import_progress):
        import_group = self._get_import_group(translatable_string, language)

        try:
            modified = translatable_string.save_translation(language)
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

    def _get_import_group(self, translatable_string, language):
        group_hash = (translatable_string.model, language)
        group_name = '{model} ({language})'.format(
            model=translatable_string.model.__name__,
            language=language
        )
        return (group_hash, group_name)
