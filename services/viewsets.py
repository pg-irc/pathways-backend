from rest_framework import viewsets
from django.core.exceptions import SuspiciousOperation
from django.http import Http404
from services import models, serializers

# pylint: disable=too-many-ancestors
class ServiceViewSet(viewsets.ReadOnlyModelViewSet):

    def get_queryset(self):
        query_params = self.request.query_params
        search_parameters = self.build_search_parameters(query_params)
        queryset = models.Service.search(search_parameters)

        if not queryset.exists():
            raise Http404

        return queryset

    def build_search_parameters(self, query_params):
        taxonomy = None
        term = None
        taxonomy_term = query_params.get('taxonomy_term', None)
        if taxonomy_term:
            if taxonomy_term.count(':') != 1:
                self.raise_taxonomy_error()
            taxonomy, term = taxonomy_term.split(':')
            if taxonomy=='' or term=='':
                self.raise_taxonomy_error()

        return {'taxonomy_id' : taxonomy, 'taxonomy_term' : term}

    def raise_taxonomy_error(self):
        raise SuspiciousOperation('Invalid argument to taxonomy_term')

    serializer_class = serializers.ServiceSerializer

# pylint: disable=too-many-ancestors
class ServiceViewSetUnderOrganizations(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        organization_id = self.kwargs['organization_id']
        return models.Service.objects.filter(organization=organization_id)

    serializer_class = serializers.ServiceSerializer
