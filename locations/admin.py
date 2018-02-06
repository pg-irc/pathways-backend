from django.contrib import admin
from locations import models

admin.site.register(models.Location)
admin.site.register(models.ServiceAtLocation)
admin.site.register(models.LocationAddress)
