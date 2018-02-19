from common.models import ValidateOnSaveMixin, RequiredCharField
from django.core import validators
from django.db import models
from parler.models import TranslatableModel, TranslatedFields
from human_services.services import private
from human_services.organizations.models import Organization
from human_services.taxonomies.models import TaxonomyTerm

class Service(ValidateOnSaveMixin, TranslatableModel):
    id = RequiredCharField(primary_key=True,
                           max_length=200,
                           validators=[validators.validate_slug])
    organization = models.ForeignKey(Organization,
                                     on_delete=models.CASCADE,
                                     related_name='services')
    taxonomy_terms = models.ManyToManyField(TaxonomyTerm,
                                            db_table='services_service_taxonomy_terms')
    translations = TranslatedFields(name=models.CharField(max_length=200),
                                    description=models.TextField(blank=True, null=True))

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name

    @classmethod
    def get_queryset(cls, search_parameters):
        queryset = cls.objects.all()
        queryset = private.add_taxonomy_filter_if_given(queryset, search_parameters)
        queryset = private.add_organization_filter_if_given(queryset, search_parameters)
        queryset = private.add_location_filter_if_given(queryset, search_parameters)
        return queryset
