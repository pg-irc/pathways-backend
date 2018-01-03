from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class ContentTranslationToolsConfig(AppConfig):
    name = 'content_translation_tools'
    verbose_name = _("Parler PO")
