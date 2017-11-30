from collections import defaultdict
from django.core.management.base import BaseCommand, CommandError
from django.db import models
from django.utils.translation import ugettext as _
from django.utils.translation import ungettext as __
import argparse
import glob
import os
import polib

from parler_po.argparse_path import argparse_path_type
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

    def handle(self, *args, **options):
        po_paths = options['po_paths']

        for po_path in po_paths:
            if os.path.isfile(po_path):
                self._import_po_file(po_path)
            elif os.path.isdir(po_path):
                self._import_translations_dir(po_path)

    def _import_translations_dir(self, translations_dir):
        po_path_search = os.path.join(
            glob.escape(translations_dir), '**', '*.po'
        )
        for po_path in glob.iglob(po_path_search, recursive=True):
            self._import_po_file(po_path)

    def _import_po_file(self, po_path):
        msg = _("Importing {}").format(po_path)
        self.stderr.write(self.style.SUCCESS(msg))

        po_file = polib.pofile(po_path)
        language_code = po_file.metadata.get('Language')

        if language_code:
            translation_entries = self._translation_entries_for_po_file(po_file)
            import_progress = ImportProgress()
            for translation_entry in translation_entries:
                self._import_translation_entry(translation_entry, language_code, import_progress)
                self._print_import_progress(import_progress, ending='\r')
            self._print_import_progress(import_progress)
        else:
            msg = _("Skipping \"{file}\": No language metadata").format(
                file=po_path
            )
            self.stderr.write(self.style.WARNING(msg))

    def _translation_entries_for_po_file(self, po_file):
        for po_entry in po_file:
            yield from TranslationEntry.from_po_entry(po_entry)

    def _import_translation_entry(self, translation_entry, language_code, import_progress):
        import_key = (translation_entry.content_type_id, language_code)

        base_translation = translation_entry.get_base_translation()

        try:
            translation = translation_entry.get_translation(language_code)
        except ValueError as error:
            msg = _("Skipping \"{field}\": {error}").format(
                field=translation_entry.instance_field_id,
                error=error
            )
            self.stderr.write(self.style.WARNING(msg))
            import_progress.add_error(import_key)
        else:
            field_id = translation_entry.field_id
            current_msgstr = getattr(translation, field_id)
            new_msgstr = translation_entry.msgstr

            if translation == base_translation:
                # Never update the base translation from a po file
                import_progress.add_skip(import_key)
            elif new_msgstr == current_msgstr:
                import_progress.add_skip(import_key)
            else:
                setattr(translation, field_id, new_msgstr)
                translation.save()
                import_progress.add_new(import_key)

    def _print_import_progress(self, import_progress, ending='\n'):
        msg = str(import_progress)
        self.stderr.write(self.style.SUCCESS(import_progress), ending=ending)

class ImportProgress(object):
    PROGRESS_ERROR = 0
    PROGRESS_NEW = 1
    PROGRESS_SKIP = 2

    def __init__(self):
        self._counts = defaultdict(lambda: defaultdict(int))

    def add_error(self, key):
        self._counts[key][None] += 1
        self._counts[key][self.PROGRESS_ERROR] += 1

    def add_new(self, key):
        self._counts[key][None] += 1
        self._counts[key][self.PROGRESS_NEW] += 1

    def add_skip(self, key):
        self._counts[key][None] += 1
        self._counts[key][self.PROGRESS_SKIP] += 1

    def __str__(self):
        return " | ".join(
            self._format_model_counts()
        )

    def _format_model_counts(self):
        for (model, counts) in self._counts.items():
            numbers_list = []

            total_count = counts[None]
            numbers_list.append(
                str(total_count)
            )

            new_count = counts[self.PROGRESS_NEW]
            if new_count:
                numbers_list.append(
                    __("({} new)", "({} new)", new_count).format(
                        new_count
                    )
                )

            error_count = counts[self.PROGRESS_ERROR]
            if error_count:
                numbers_list.append(
                    __("({} error)", "({} errors)", error_count).format(
                        error_count
                    )
                )

            yield _("{model}: {numbers}").format(
                model=model,
                numbers=" ".join(numbers_list)
            )
