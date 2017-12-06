from django.contrib import admin
from taxonomies import models


@admin.register(models.Taxonomy)
class TaxonomyAdmin(admin.ModelAdmin):
    list_display = ('vocabulary', 'name',)
    list_filter = [
        'vocabulary',
    ]
