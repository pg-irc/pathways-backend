from rest_framework import viewsets
from django.utils.decorators import method_decorator
from human_services.services import models, serializers, private, documentation


class SearchParameters:
    def __init__(self, query_parameters, path_parameters):
        self.taxonomy_terms = private.parse_taxonomy_parameter(query_parameters)
        self.organization_id = path_parameters.get('organization_id', None)
        self.location_id = path_parameters.get('location_id', None)


# pylint: disable=too-many-ancestors
@method_decorator(name='list', decorator=documentation.get_list_schema_decorator())
class ServiceViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = serializers.ServiceSerializer
    search_fields = ('translations__name', 'translations__description',)
    ordering_fields = '__all__'

    def get_queryset(self):
        query_parameters = self.request.query_params
        path_parameters = self.kwargs
        search_parameters = SearchParameters(query_parameters, path_parameters)
        return models.Service.get_queryset(search_parameters)
