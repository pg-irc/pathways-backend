from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class ParlerPOConfig(AppConfig):
    name = 'parler_po'
    verbose_name = _("Parler PO")
