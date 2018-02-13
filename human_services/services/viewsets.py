from rest_framework import viewsets
from human_services.services import models, serializers, private, documentation

class SearchParameters:
    def __init__(self, query_parameters, path_parameters):
        self.taxonomy_id, self.taxonomy_term = private.parse_taxonomy_parameter(query_parameters)
        self.organization_id = path_parameters.get('organization_id', None)

# pylint: disable=too-many-ancestors
class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    schema = documentation.get_list_endpoint_fields()
    search_fields = ('translations__name', 'translations__description',)
    ordering_fields = '__all__'

    def get_queryset(self):
        query_parameters = self.request.query_params
        path_parameters = self.kwargs
        search_parameters = SearchParameters(query_parameters, path_parameters)
        queryset = models.Service.get_queryset(search_parameters)
        return queryset

    serializer_class = serializers.ServiceSerializer
