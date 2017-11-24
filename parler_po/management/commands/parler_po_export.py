from datetime import datetime
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext_lazy as _
from parler.models import TranslatableModel
import argparse
import itertools
import os
import polib

PARLER_PO_CONTACT = getattr(settings, 'PARLER_PO_CONTACT', None)

class Command(BaseCommand):
    help = 'Export PO files for all translatable content'

    def add_arguments(self, parser):
        parser.add_argument(
            'output_dir',
            type=argparse_dir_type,
            metavar='output'
        )

    def handle(self, *args, **options):
        output_dir = options['output_dir']

        for (domain, model) in self._translatable_models():
            domain_entries = dict()
            model_translations = self._get_model_translations(model)

            for (translation, instance_po_entries) in model_translations:
                translation_id = translation.language_code if translation else None
                po_entries = domain_entries.setdefault(translation_id, list())
                po_entries.extend(instance_po_entries)

            pot_entries = domain_entries.pop(None, list())
            pot_path = self._get_pot_path(output_dir, domain)
            pot_file = self._update_pot_file(pot_path, pot_entries)

            for (translation, po_entries) in domain_entries.items():
                po_path = self._get_po_path(output_dir, domain, translation)
                self._update_po_file(po_path, po_entries, pot_file)

    def _translatable_models(self):
        for contenttype in ContentType.objects.all():
            model_class = contenttype.model_class()
            if issubclass(model_class, TranslatableModel):
                domain = '.'.join([contenttype.app_label, contenttype.model])
                yield (domain, model_class)

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

    def _get_pot_path(self, output_dir, domain):
        pot_name = '{}.pot'.format(domain)
        return os.path.join(output_dir, pot_name)

    def _get_po_path(self, output_dir, domain, language_code):
        po_name = '{}.po'.format(domain)
        language_dir = os.path.join(output_dir, language_code)
        os.makedirs(language_dir, exist_ok=True)
        return os.path.join(language_dir, po_name)

    def _update_pot_file(self, po_path, po_entries):
        now_str = datetime.utcnow().isoformat()

        pot_file = polib.POFile()
        pot_file.metadata = dict()

        pot_file.metadata['Project-Id-Version'] = '1.0'
        pot_file.metadata['Report-Msgid-Bugs-To'] = PARLER_PO_CONTACT
        pot_file.metadata['POT-Creation-Date'] = now_str
        pot_file.metadata['MIME-Version'] = '1.0'
        pot_file.metadata['Content-Type'] = 'text/plain; charset=utf-8'
        pot_file.metadata['Content-Transfer-Encoding'] = '8bit'

        pot_file.extend(po_entries)

        pot_file.save(po_path)

        return pot_file

    def _update_po_file(self, po_path, po_entries, pot_file):
        now_str = datetime.utcnow().isoformat()

        po_file = polib.POFile()
        po_file.metadata = dict()

        po_file.metadata.update(pot_file.metadata)
        po_file.metadata['PO-Revision-Date'] = now_str

        po_file.metadata['MIME-Version'] = '1.0'
        po_file.metadata['Content-Type'] = 'text/plain; charset=utf-8'
        po_file.metadata['Content-Transfer-Encoding'] = '8bit'

        po_file.extend(po_entries)
        po_file.merge(pot_file)

        po_file.save(po_path)

        return po_file

def argparse_dir_type(dir_name):
    dir_path = os.path.abspath(dir_name)

    if os.path.exists(dir_path):
        if not os.path.isdir(dir_path):
            msg = _("The path {} must be a directory").format(dir_path)
            raise argparse.ArgumentTypeError(msg)
        elif not os.access(dir_path, os.W_OK):
            msg = _("The directory {} must be writable").format(dir_path)
            raise argparse.ArgumentTypeError(msg)
        else:
            return dir_path
    else:
        try:
            os.makedirs(dir_path)
        except OSError as e:
            msg = _("The directory {} does not exist").format(dir_path)
            raise argparse.ArgumentTypeError(msg)
        else:
            return dir_path
