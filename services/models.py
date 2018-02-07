from common.models import ValidateOnSaveMixin, RequiredCharField
from django.core import validators
from django.db import models
from django.db.models import Q
from human_services.organizations.models import Organization
from parler.models import TranslatableModel, TranslatedFields
from taxonomies.models import TaxonomyTerm
from services import details

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
        queryset = cls.add_full_text_search_filter_if_given(queryset, search_parameters)
        queryset = cls.add_sorting_if_given(queryset, search_parameters)
        return queryset

    @staticmethod
    def add_taxonomy_filter_if_given(queryset, search_parameters):
        identifier = search_parameters.taxonomy_id
        term = search_parameters.taxonomy_term

        if identifier and term:
            queryset = queryset.filter(taxonomy_terms__taxonomy_id=identifier,
                                       taxonomy_terms__name=term)
        return queryset

    @staticmethod
    def add_full_text_search_filter_if_given(queryset, search_parameters):
        search_terms = search_parameters.full_text_search_terms
        if not search_terms:
            return queryset

        builder = details.FilterBuilder()
        for term in search_terms:
            builder.add_with_or(Q(translations__name__icontains=term),
                                Q(translations__description__icontains=term))

        return queryset.filter(builder.get_filter())

    @classmethod
    def add_sorting_if_given(cls, queryset, search_parameters):
        sort_arguments = search_parameters.sort_by

        if not sort_arguments:
            return queryset

        sort_arguments = [cls.add_prefix_on_translated_fields(argument) for argument in sort_arguments]

        return queryset.order_by(*sort_arguments)

    @classmethod
    def add_prefix_on_translated_fields(cls, argument):
        reverse_sort = argument[0:1] == '-'
        stripped_argument = argument[1:] if reverse_sort else argument

        translated_fields = ['name', 'description']
        if stripped_argument not in translated_fields:
            return argument

        argument = 'translations__' + stripped_argument
        return '-' + argument if reverse_sort else argument
