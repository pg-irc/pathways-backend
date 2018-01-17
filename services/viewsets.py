from rest_framework import viewsets
from django.core.exceptions import SuspiciousOperation
from services import models, serializers

# pylint: disable=too-many-ancestors
class ServiceViewSet(viewsets.ReadOnlyModelViewSet):

    def get_queryset(self):
        query_params = self.request.query_params
        queryset = models.Service.objects.all()

        queryset = self.add_taxonomy_filter_if_given(query_params, queryset)

        return queryset

    def add_taxonomy_filter_if_given(self, query_params, queryset):
        taxonomy_term = query_params.get('taxonomy_term', None)
        if taxonomy_term:
            queryset = self.add_taxonomy_filter(queryset, taxonomy_term)
        return queryset

    def add_taxonomy_filter(self, queryset, parameter):
        taxonomy, term = self.parse_taxonomy_parameter(parameter)
        return (queryset.filter(taxonomy_terms__name=term).
                         filter(taxonomy_terms__taxonomy_id=taxonomy))

    def parse_taxonomy_parameter(self, parameter):
        if parameter.count(':') != 1:
            self.raise_taxonomy_error()
        taxonomy, term = parameter.split(':')
        if taxonomy=='' or term=='':
            self.raise_taxonomy_error()
        return taxonomy, term

    def raise_taxonomy_error(self):
        raise SuspiciousOperation('Invalid argument to taxonomy_term')

    serializer_class = serializers.ServiceSerializer

# pylint: disable=too-many-ancestors
class ServiceViewSetUnderOrganizations(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        organization_id = self.kwargs['organization_id']
        return models.Service.objects.filter(organization=organization_id)

    serializer_class = serializers.ServiceSerializer
