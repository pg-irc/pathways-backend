from django.core.management.base import BaseCommand, CommandError
from django.db import models
from django.utils.translation import ugettext_lazy as _
import argparse
import glob
import os
import polib

from parler_po.argparse_path import argparse_path_type
from parler_po.util import (TranslationEntry, get_base_translation)

class Command(BaseCommand):
    help = _("Import a set of PO files with new content translations")

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

        # Get locale directories in translations_dir.
        # For each locale directory, get PO files inside LC_MESSAGES.

    def _import_translations_dir(self, translations_dir):
        po_path_search = os.path.join(
            glob.escape(translations_dir), '**', '*.po'
        )
        for po_path in glob.iglob(po_path_search):
            self._import_po_file(po_path)

    def _import_po_file(self, po_path):
        msg = _("Importing file {}").format(po_path)
        self.stdout.write(self.style.NOTICE(po_path))
        po_file = polib.pofile(po_path)
        language_code = po_file.metadata.get('Language')

        if language_code:
            for po_entry in po_file:
                for translation_entry in TranslationEntry.from_po_entry(po_entry):
                    translatable = translation_entry.instance
                    base_translation = get_base_translation(translatable)

                    try:
                        translation = translatable.get_translation(language_code)
                    except translatable.translations.model.DoesNotExist:
                        translatable.create_translation(language_code)
                        translation = translatable.get_translation(language_code)

                    base_msgid = getattr(base_translation, translation_entry.field_id)
                    if base_msgid == translation_entry.msgid:
                        setattr(translation, translation_entry.field_id, translation_entry.msgstr)
                    else:
                        msg = _("Translation for \"{field}\" has incorrect msgid").format(
                            field=translation_entry.instance_field_id
                        )
                        self.stderr.write(self.style.WARNING(msg))
        else:
            msg = _("PO file \"{}\" has no language")
            self.stderr.write(self.style.WARNING(msg))
