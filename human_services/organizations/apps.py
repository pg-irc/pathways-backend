from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class OrganizationsConfig(AppConfig):
    name = 'human_services.organizations'
    verbose_name = _('Organizations')
