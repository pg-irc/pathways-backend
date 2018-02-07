from django.contrib import admin
from human_services.addresses import models

admin.site.register(models.Address)
admin.site.register(models.AddressType)
