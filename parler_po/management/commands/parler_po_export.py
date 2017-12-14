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
            dest='locales',
            type=str,
            action='append'
        )

        parser.add_argument(
            '--all-locales',
            dest='all_locales',
            action='store_true'
        )

    def handle(self, *args, **options):
        translations_dir = options['translations_dir']
        locales_list = options['locales']
        all_locales = options['all_locales']

        for model in all_translatable_models():
            if all_locales:
                model_po_entries = self._model_po_entries(model)
            elif locales_list:
                model_po_entries = self._model_po_entries(model, locales=locales_list)
            else:
                model_po_entries = self._model_po_entries(model, locales=[])

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

    def _model_po_entries(self, model, locales=None):
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
        # TODO: Move this somewhere else.
        #       Raise an error if instance is not a translatable model.

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
        fields_list = translation.get_translated_fields()

        for field_id in fields_list:
            try:
                translatable_string = TranslatableString.from_translation(
                    translation,
                    field_id
                )
            except ParlerPOError as error:
                if getattr(translation, field_id, None):
                    self.stderr.write(
                        _("Skipping \"{translation} - {field_id}\": {error}").format(
                            translation=translation.master,
                            field_id=field_id,
                            error=error
                        )
                    )
                else:
                    pass
            else:
                po_entry = translatable_string.as_po_entry()
                if strip_msgstr:
                    po_entry.msgstr = ''
                yield po_entry
