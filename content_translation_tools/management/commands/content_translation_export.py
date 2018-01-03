from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext as _
import argparse
import sys

from content_translation_tools.exceptions import ContentTranslationToolsError, ModelNotTranslatableError
from content_translation_tools.field_ids import parse_model_id
from content_translation_tools.po_file import create_po_file_for_model, create_pot_file_for_model
from content_translation_tools.queries import is_translatable_model

class Command(BaseCommand):
    help = _("Export a PO file for a translatable model")

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            dest='file',
            nargs='?',
            type=argparse.FileType('w'),
            default=sys.stdout
        )

        parser.add_argument(
            'model',
            nargs='+'
        )

        parser.add_argument(
            '-l', '--language',
            dest='language',
            default=None
        )

    def handle(self, *args, **options):
        model_ids = options['model']
        language = options['language']
        out_file = options['file']

        models = map(self._get_model_from_model_id, model_ids)

        for model in models:
            self._export_model_po(model, language, out_file)

    def _get_model_from_model_id(self, model_id):
        try:
            return _parse_translatable_model_id(model_id)
        except ContentTranslationToolsError as error:
            raise CommandError(error)

    def _export_model_po(self, model, language, out_file):
        errors_list = []

        if language:
            po_file = create_po_file_for_model(model, language, errors_out=errors_list)
        else:
            po_file = create_pot_file_for_model(model, errors_out=errors_list)

        for error in errors_list:
            self.stderr.write(error)

        out_file.write(str(po_file))

def _parse_translatable_model_id(model_id):
    model = parse_model_id(model_id)

    if not is_translatable_model(model):
        raise ModelNotTranslatableError(model)

    return model
