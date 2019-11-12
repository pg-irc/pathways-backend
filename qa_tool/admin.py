from django.contrib import admin
from qa_tool.models import Algorithm, SearchLocation, RelevancyScore

admin.site.register(Algorithm)
admin.site.register(SearchLocation)
admin.site.register(RelevancyScore)
