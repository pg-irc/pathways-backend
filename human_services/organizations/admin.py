from django.contrib import admin
from parler.admin import TranslatableAdmin
from human_services.organizations import models

class OrganizationAdmin(TranslatableAdmin):
    pass

admin.site.register(models.Organization, OrganizationAdmin)
