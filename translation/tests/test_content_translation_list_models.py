from django.core.management import call_command
from django.test import TestCase, override_settings
from unittest.mock import patch

from human_services.organizations.models import Organization
import io

TEST_PARLER_PO_CONTACT = 'test_content_translation_export@example.com'

class ContentTranslationToolsListModelsTests(TestCase):
    def test_lists_translatable_models(self):
        with patch('translation.management.commands.content_translation_list_models.all_translatable_models') as all_translatable_models:
            all_translatable_models.return_value = [Organization]
            stdout, stderr = _run_content_translation_list_models()
            self.assertEqual(stdout.getvalue(), 'organizations.organization\n')

@override_settings(PARLER_PO_CONTACT=TEST_PARLER_PO_CONTACT)
def _run_content_translation_list_models(*args, **kwargs):
    stdout = io.StringIO()
    stderr = io.StringIO()
    call_command('content_translation_list_models', *args, **kwargs, stdout=stdout, stderr=stderr)
    return stdout, stderr
