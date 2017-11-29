from collections import defaultdict
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy as _
from parler.models import TranslatableModel
import itertools

from parler_po.argparse_path import argparse_path_type
from parler_po.util import (
    TranslationEntry,
    content_type_id,
    get_base_translation,
    get_pot_path,
    get_po_path,
    new_pot_file,
    new_po_file
)

class Command(BaseCommand):
    help = _("Export PO files for all translatable content")

    def add_arguments(self, parser):
        parser.add_argument(
            'translations_dir',
            type=argparse_path_type('dir', 'w'),
            metavar='directory'
        )

        parser.add_argument(
            '-l', '--locale',
            dest='locales',
            type=str,
            action='append'
        )

        parser.add_argument(
            '--all-locales',
            dest='all_locales',
            type=bool,
            const=True,
            nargs='?'
        )

    def handle(self, *args, **options):
        translations_dir = options['translations_dir']
        locales_list = options['locales']
        all_locales = options['all_locales']

        for model in self._translatable_models():
            if all_locales:
                model_po_entries = self._model_po_entries(model)
            elif locales_list:
                model_po_entries = self._model_po_entries(model, locales=locales_list)
            else:
                model_po_entries = self._model_po_entries(model, locales=[])

            pot_entries = model_po_entries.pop(None, list())
            pot_path = get_pot_path(translations_dir, model)
            pot_file = new_pot_file()
            pot_file.extend(pot_entries)
            pot_file.save(pot_path)

            for (language_code, po_entries) in model_po_entries.items():
                po_path = get_po_path(translations_dir, model, language_code)
                po_file = new_po_file(pot_file=pot_file, language_code=language_code)
                po_file.extend(po_entries)
                po_file.merge(pot_file)
                po_file.save(po_path)

    def _translatable_models(self):
        for content_type in ContentType.objects.all():
            model_class = content_type.model_class()
            if issubclass(model_class, TranslatableModel):
                yield model_class

    def _model_po_entries(self, model, locales=None):
        model_po_entries = defaultdict(list)

        for instance in model.objects.all():
            instance_po_entries = self._translatable_po_entries(instance, locales)
            for (language_code, po_entries) in instance_po_entries:
                model_po_entries[language_code].append(po_entries)

        return {
            language_code: itertools.chain.from_iterable(po_entries)
            for language_code, po_entries in model_po_entries.items()
        }

    def _translatable_po_entries(self, translatable, locales=None):
        base_translation = get_base_translation(translatable)

        if base_translation:
            pot_entries = self._translation_po_entries(
                translatable,
                base_translation
            )
            yield (None, pot_entries)

            if locales is None:
                translations_query = translatable.translations.all()
            else:
                translations_query = translatable.translations.filter(
                    language_code__in=locales
                )

            for translation in translations_query:
                po_entries = self._translation_po_entries(
                    translatable,
                    base_translation,
                    translation=translation
                )
                yield (translation.language_code, po_entries)
        else:
            msg = _("Skipping \"{record}\": missing base translation").format(
                record=translatable
            )
            self.stderr.write(self.style.WARNING(msg))

    def _translation_po_entries(self, translatable, base_translation, translation=None):
        for field_id in base_translation.get_translated_fields():
            msgid = getattr(base_translation, field_id)
            msgstr = getattr(translation, field_id) if translation else ""
            translation_entry = TranslationEntry(
                translatable, field_id, msgid, msgstr
            )
            yield translation_entry.as_po_entry()
