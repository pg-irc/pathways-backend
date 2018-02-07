from django.contrib import admin
from human_services.taxonomies import models


@admin.register(models.TaxonomyTerm)
class TaxonomyTermAdmin(admin.ModelAdmin):
    list_display = ('taxonomy_id', 'name',)
    list_filter = [
        'taxonomy_id',
    ]
