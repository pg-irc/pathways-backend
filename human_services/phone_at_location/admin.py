from django.contrib import admin
from human_services.phone_at_location import models

admin.site.register(models.PhoneNumberType)
admin.site.register(models.PhoneAtLocation)
