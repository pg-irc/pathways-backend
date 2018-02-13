from common.models import ValidateOnSaveMixin, RequiredCharField
from django.core import validators
from django.db import models
from django.db.models import Q
from human_services.organizations.models import Organization
from parler.models import TranslatableModel, TranslatedFields
from human_services.taxonomies.models import TaxonomyTerm
from . import private

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
        queryset = cls.add_taxonomy_filter_if_given(queryset, search_parameters)
        queryset = cls.add_organization_filter_if_given(queryset, search_parameters)
        queryset = cls.add_location_filter_if_given(queryset, search_parameters)
        return queryset

    @staticmethod
    def add_taxonomy_filter_if_given(queryset, search_parameters):
        identifier = search_parameters.taxonomy_id
        term = search_parameters.taxonomy_term

        if identifier and term:
            queryset = queryset.filter(taxonomy_terms__taxonomy_id=identifier,
                                       taxonomy_terms__name=term)
        return queryset

    def add_organization_filter_if_given(queryset, search_parameters):
        if search_parameters.organization_id:
            queryset = queryset.filter(organization_id=search_parameters.organization_id)
        return queryset

    def add_location_filter_if_given(queryset, search_parameters):
        if search_parameters.location_id:
            queryset = queryset.filter(serviceatlocation__location_id=search_parameters.location_id)
        return queryset
