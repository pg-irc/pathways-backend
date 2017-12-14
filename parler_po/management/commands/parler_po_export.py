from collections import defaultdict
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.utils.translation import ugettext as _
from parler.models import TranslatableModel
import itertools

from parler_po.argparse_path import argparse_path_type
from parler_po.exceptions import ParlerPOError
from parler_po.po_file import create_po_file, create_pot_file
from parler_po.queries import all_translatable_models, get_base_translation
from parler_po.translatable_string import TranslatableString

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
            dest='locales_list',
            type=str,
            default=[],
            action='append'
        )

        parser.add_argument(
            '--all-locales',
            dest='all_locales',
            action='store_true'
        )

    def handle(self, *args, **options):
        translations_dir = options['translations_dir']
        locales_list = options['locales_list']
        all_locales = options['all_locales']

        locales_to_process = None if all_locales else locales_list

        for model in all_translatable_models():
            model_po_entries = self._po_entries_for_translatable_model(model, locales_to_process)

            pot_entries = model_po_entries.pop(None, list())
            pot_file = create_pot_file(
                translations_dir,
                model,
                pot_entries
            )

            for (language_code, po_entries) in model_po_entries.items():
                create_po_file(
                    translations_dir,
                    model,
                    po_entries,
                    language_code,
                    pot_file
                )

    def _po_entries_for_translatable_model(self, model, locales=None):
        model_po_entries = defaultdict(list)

        for instance in model.objects.all():
            instance_po_entries = self._po_entries_for_translatable_instance(instance, locales)
            for (language_code, po_entries) in instance_po_entries:
                model_po_entries[language_code].append(po_entries)

        return {
            language_code: itertools.chain.from_iterable(po_entries)
            for language_code, po_entries in model_po_entries.items()
        }

    def _po_entries_for_translatable_instance(self, instance, locales=None):
        base_translation = get_base_translation(instance)

        if base_translation:
            pot_entries = self._po_entries_for_translation(base_translation, strip_msgstr=True)
            yield (None, pot_entries)

        if locales is None:
            translations_query = instance.translations.all()
        else:
            translations_query = instance.translations.filter(
                language_code__in=locales
            )

        for translation in translations_query:
            po_entries = self._po_entries_for_translation(translation)
            yield (translation.language_code, po_entries)

    def _po_entries_for_translation(self, translation, strip_msgstr=False):
        errors_list = []

        translatable_strings = TranslatableString.all_from_translation(
            translation, errors_out=errors_list
        )

        for translatable_string in translatable_strings:
            yield translatable_string.as_po_entry(strip_msgstr)

        for error in errors_list:
            self.stderr.write(error)
