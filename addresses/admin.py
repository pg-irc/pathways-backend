from django.contrib import admin
from addresses import models

admin.site.register(models.Address)
admin.site.register(models.AddressType)
