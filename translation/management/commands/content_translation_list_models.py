from django.core.management.base import BaseCommand
from django.utils.translation import ugettext as _

from translation.field_ids import build_model_id
from translation.queries import all_translatable_models

class Command(BaseCommand):
    help = _('List all translatable models for use with content_translation_export')

    def handle(self, *args, **options):
        models = all_translatable_models()
        model_ids = map(build_model_id, models)
        self.stdout.write('\n'.join(model_ids))
