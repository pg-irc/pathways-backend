from django.contrib import admin
from parler.admin import TranslatableAdmin
from human_services.locations import models

class ServiceAtLocationAdmin(admin.ModelAdmin):
    raw_id_fields = ['service', 'location']

admin.site.register(models.ServiceAtLocation, ServiceAtLocationAdmin)

class LocationAdmin(TranslatableAdmin):
    raw_id_fields = ['organization']

admin.site.register(models.Location, LocationAdmin)

class LocationAddressAdmin(admin.ModelAdmin):
    raw_id_fields = ['address', 'location']
    radio_fields = {'address_type': admin.VERTICAL}

admin.site.register(models.LocationAddress, LocationAddressAdmin)
