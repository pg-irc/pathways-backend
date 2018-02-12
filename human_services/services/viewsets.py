from rest_framework import viewsets
from human_services.services import models, serializers, private, documentation

class SearchParameters:
    def __init__(self, query_parameters):
        self.taxonomy_id, self.taxonomy_term = private.parse_taxonomy_parameter(query_parameters)

# pylint: disable=too-many-ancestors
class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    schema = documentation.get_list_endpoint_fields()
    search_fields = ('translations__name', 'translations__description',)
    ordering_fields = '__all__'

    def get_queryset(self):
        query_parameters = self.request.query_params
        search_parameters = SearchParameters(query_parameters)
        queryset = models.Service.get_queryset(search_parameters)
        return queryset

    serializer_class = serializers.ServiceSerializer

# pylint: disable=too-many-ancestors
class ServiceViewSetUnderOrganizations(viewsets.ReadOnlyModelViewSet):
    schema = documentation.get_list_endpoint_fields()

    def get_queryset(self):
        organization_id = self.kwargs['organization_id']
        return models.Service.objects.filter(organization=organization_id)

    serializer_class = serializers.ServiceSerializer
