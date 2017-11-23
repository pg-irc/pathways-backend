from django.contrib import admin
from parler.admin import TranslatableAdmin
from service_providers import models

class ServiceProvidersAdmin(TranslatableAdmin):
    pass

admin.site.register(models.ServiceProvider, TranslatableAdmin)
