from django.contrib import admin
from .models import Algorithm, SearchLocation, RelevancyScore

admin.site.register(Algorithm)
admin.site.register(SearchLocation)
admin.site.register(RelevancyScore)
