from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, CommandError
from parler.models import TranslatableModel
import argparse
import polib

class Command(BaseCommand):
    help = 'Export PO files for all translatable content'

    def add_arguments(self, parser):
        parser.add_argument(
            '-o', '--pot-file',
            type=argparse.FileType('w'),
            default='-',
            metavar='file'
        )

    def handle(self, *args, **options):
        pot_file = options['pot_file']

        pot_data = polib.POFile()
        pot_data.metadata = {
            'Project-Id-Version': '1.0',
            'Report-Msgid-Bugs-To': 'you@example.com',
            'POT-Creation-Date': '2007-10-18 14:00+0100',
            'PO-Revision-Date': '2007-10-18 14:00+0100',
            'Last-Translator': 'you <you@example.com>',
            'Language-Team': 'English <yourteam@example.com>',
            'MIME-Version': '1.0',
            'Content-Type': 'text/plain; charset=utf-8',
            'Content-Transfer-Encoding': '8bit',
        }

        for model in self._translatable_models():
            model_translations = self._get_model_translations(model)
            for (translation, po_entries) in model_translations:
                # TODO: Write to LANG.po
                pot_data.extend(po_entries)

        pot_file.write(str(pot_data))

    def _translatable_models(self):
        for contenttype in ContentType.objects.all():
            model_class = contenttype.model_class()
            if issubclass(model_class, TranslatableModel):
                yield model_class

    def _get_model_translations(self, model):
        for instance in model.objects.all():
            base_po_entries = self._get_po_entries(instance)
            yield (None, base_po_entries)
            for translation in instance.translations.all():
                po_entries = self._get_po_entries(instance, translation)
                yield (translation, po_entries)

    def _get_po_entries(self, translatable, translation=None):
        base_language = 'en'
        prefix = translatable.__class__.__name__
        base_translation = translatable.get_translation(base_language)
        translated_fields = base_translation.get_translated_fields()

        is_translated = bool(translation and translation != base_translation)

        for field in translated_fields:
            msgid = getattr(base_translation, field)
            msgstr = getattr(translation, field) if is_translated else ""
            field_name = '.'.join([prefix, field])

            yield polib.POEntry(
                msgid=msgid,
                msgstr=msgstr,
                occurrences=[(field_name, translatable.pk)]
            )
