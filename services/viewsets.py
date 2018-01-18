from rest_framework import viewsets
from django.core.exceptions import SuspiciousOperation
from django.http import Http404
from services import models, serializers

class SearchParameters:
    def __init__(self, query_parameters):
        self.taxonomy_id, self.taxonomy_term = self.parse_taxonomy_parameter(query_parameters)

    def parse_taxonomy_parameter(self, query_parameters):
        taxonomy_term = query_parameters.get('taxonomy_term', None)
        if not taxonomy_term:
            return None, None
        return self.build_valid_taxonomy_parameters(taxonomy_term)

    def build_valid_taxonomy_parameters(self, taxonomy_term):
        if taxonomy_term.count(':') != 1:
            self.raise_taxonomy_error()

        taxonomy_id, term = taxonomy_term.split(':')
        if taxonomy_id == '' or term == '':
            self.raise_taxonomy_error()

        return taxonomy_id, term

    def raise_taxonomy_error(self):
        raise SuspiciousOperation('Invalid argument to taxonomy_term')

# pylint: disable=too-many-ancestors
class ServiceViewSet(viewsets.ReadOnlyModelViewSet):

    def get_queryset(self):
        query_parameters = self.request.query_params
        search_parameters = SearchParameters(query_parameters)
        queryset = models.Service.get_queryset(search_parameters)

        if not queryset.exists():
            raise Http404

        return queryset

    serializer_class = serializers.ServiceSerializer

# pylint: disable=too-many-ancestors
class ServiceViewSetUnderOrganizations(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        organization_id = self.kwargs['organization_id']
        return models.Service.objects.filter(organization=organization_id)

    serializer_class = serializers.ServiceSerializer
