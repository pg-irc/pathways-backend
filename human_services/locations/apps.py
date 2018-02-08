from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class LocationsConfig(AppConfig):
    name = 'human_services.locations'
    verbose_name = _('Locations')
