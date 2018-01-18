from rest_framework import viewsets
from django.core.exceptions import SuspiciousOperation
from django.http import Http404
from services import models, serializers

class SearchParameters:
    def __init__(self, query_parameters):
        self.taxonomy_id = None
        self.taxonomy_term = None
        taxonomy_term = query_parameters.get('taxonomy_term', None)
        if taxonomy_term:
            if taxonomy_term.count(':') != 1:
                self.raise_taxonomy_error()
            self.taxonomy_id, self.taxonomy_term = taxonomy_term.split(':')
            if self.taxonomy_id=='' or self.taxonomy_term=='':
                self.raise_taxonomy_error()

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
