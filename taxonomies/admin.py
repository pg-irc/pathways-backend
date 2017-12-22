from django.contrib import admin
from taxonomies import models


@admin.register(models.TaxonomyTerm)
class TaxonomyTermAdmin(admin.ModelAdmin):
    list_display = ('taxonomy_id', 'name',)
    list_filter = [
        'taxonomy_id',
    ]
