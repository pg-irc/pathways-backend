from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class TaxonomiesConfig(AppConfig):
    name = 'human_services.taxonomies'
    verbose_name = _("Taxonomies")
