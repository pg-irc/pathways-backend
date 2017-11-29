from collections import defaultdict
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
            all_model_counts = defaultdict(lambda: defaultdict(int))

            for po_entry in po_file:
                for translation_entry in TranslationEntry.from_po_entry(po_entry):
                    model_key = "{type_id} ({language})".format(
                        type_id=translation_entry.content_type_id,
                        language=language_code
                    )
                    model_counts = all_model_counts[model_key]

                    model_counts['total'] += 1

                    translatable = translation_entry.instance
                    base_translation = get_base_translation(translatable)

                    try:
                        translation = translatable.get_translation(language_code)
                    except translatable.translations.model.DoesNotExist:
                        translatable.create_translation(language_code)
                        translation = translatable.get_translation(language_code)

                    base_msgid = getattr(base_translation, translation_entry.field_id)
                    current_msgstr = getattr(translation, translation_entry.field_id)

                    if base_msgid != translation_entry.msgid:
                        model_counts['error'] += 1
                        msg = _("Skipping \"{field}\": incorrect msgid").format(
                            field=translation_entry.instance_field_id
                        )
                        self.stderr.write(self.style.WARNING(msg))
                    elif translation_entry.msgstr != current_msgstr:
                        model_counts['new'] += 1
                        setattr(translation, translation_entry.field_id, translation_entry.msgstr)
                        translation.save()
                    else:
                        model_counts['skip'] += 1

                    model_counts_list = []

                    for (model, counts) in all_model_counts.items():
                        model_counts_list.append(
                            _("{model}: {success} / {total} (+{new})").format(
                                model=model,
                                success=counts['new'] + counts['skip'],
                                new=counts['new'],
                                total=counts['total']
                            )
                        )

                    msg = " | ".join(model_counts_list)
                    self.stderr.write(self.style.SUCCESS(msg), ending='\r')
            self.stderr.write('\n')
        else:
            msg = _("Skipping \"{file}\": no language metadata").format(
                file=po_path
            )
            self.stderr.write(self.style.WARNING(msg))
