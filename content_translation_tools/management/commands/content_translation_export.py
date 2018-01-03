from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext as _
import argparse
import sys

from content_translation_tools.exceptions import ContentTranslationToolsError
from content_translation_tools.po_file import create_po_file_for_model, create_pot_file_for_model
from content_translation_tools.queries import all_translatable_models
from content_translation_tools.field_ids import build_model_id, parse_model_id

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

        model_group = parser.add_mutually_exclusive_group(required=True)

        model_group.add_argument(
            'model',
            nargs='*',
            default=[]
        )

        model_group.add_argument(
            '--list-models',
            dest='list_models',
            action='store_true'
        )

        type_group = parser.add_mutually_exclusive_group()

        type_group.add_argument(
            '-l', '--language',
            dest='language'
        )

        type_group.add_argument(
            '-t', '--pot',
            dest='language',
            const=None,
            action='store_const'
        )

    def handle(self, *args, **options):
        model_ids = options['model']
        list_models = options['list_models']
        language = options['language']
        out_file = options['file']

        if model_ids:
            self.export_model_list(model_ids, language, out_file)
        elif list_models:
            self.list_models()

    def export_model_list(self, model_ids, language, out_file):
        for model_id in model_ids:
            self.export_model(model_id, language, out_file)

    def export_model(self, model_id, language, out_file):
        try:
            model = parse_model_id(model_id)
        except ContentTranslationToolsError as error:
            raise CommandError(error)

        errors_list = []

        if language is None:
            po_file = create_pot_file_for_model(model, errors_out=errors_list)
        else:
            po_file = create_po_file_for_model(model, language, errors_out=errors_list)

        for error in errors_list:
            self.stderr.write(error)

        out_file.write(str(po_file))

    def list_models(self):
        for model in all_translatable_models():
            self.stdout.write(build_model_id(model))
