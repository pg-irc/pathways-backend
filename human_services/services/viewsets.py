from rest_framework import viewsets
from human_services.services import models, serializers
import human_services.services.details as details

class SearchParameters:
    def __init__(self, query_parameters):
        self.taxonomy_id, self.taxonomy_term = details.parse_taxonomy_parameter(query_parameters)
        self.full_text_search_terms = details.parse_full_text_search_terms(query_parameters)
        self.sort_by = details.parse_sorting(query_parameters)

# pylint: disable=too-many-ancestors
class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        query_parameters = self.request.query_params
        search_parameters = SearchParameters(query_parameters)
        queryset = models.Service.get_queryset(search_parameters)
        return queryset

    serializer_class = serializers.ServiceSerializer

# pylint: disable=too-many-ancestors
class ServiceViewSetUnderOrganizations(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        organization_id = self.kwargs['organization_id']
        return models.Service.objects.filter(organization=organization_id)

    serializer_class = serializers.ServiceSerializer
