from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class ServicesConfig(AppConfig):
    name = 'human_services.services'
    verbose_name = _('Services')
