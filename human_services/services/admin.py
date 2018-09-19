from django.contrib import admin
from parler.admin import TranslatableAdmin
from human_services.services import models

class ServiceAdmin(TranslatableAdmin):
    raw_id_fields = ['organization', 'taxonomy_terms']

admin.site.register(models.Service, ServiceAdmin)
