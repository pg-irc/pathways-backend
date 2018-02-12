from rest_framework import viewsets, filters
from human_services.services import models, serializers
from human_services.services import private
from human_services.services import documentation

class SearchParameters:
    def __init__(self, query_parameters):
        self.taxonomy_id, self.taxonomy_term = private.parse_taxonomy_parameter(query_parameters)


class MySearchFilter(filters.SearchFilter):
    search_description = 'Search terms for full test search, one or more terms separated by space or comma, logical AND implied among the terms'

REVERSE_PREFIX = '-'

class MyOrderingFilter(filters.OrderingFilter):
    ordering_description = 'Which field to use when ordering the results.'


    def get_ordering(self, request, queryset, view):
        argument_string = request.query_params.get(self.ordering_param)
        if argument_string:
            arguments = argument_string.replace(',', ' ').split()
            return [self.set_prefix(argument) for argument in arguments if argument]
        return None

    def set_prefix(self, argument):
        argument = argument.strip()
        reverse_sort = argument[0:1] == REVERSE_PREFIX
        stripped_argument = argument[1:] if reverse_sort else argument

        translated_fields = ['name', 'description']
        if stripped_argument not in translated_fields:
            return argument

        argument = 'translations__' + stripped_argument
        return REVERSE_PREFIX + argument if reverse_sort else argument

# pylint: disable=too-many-ancestors
class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    schema = documentation.get_list_endpoint_fields()
    filter_backends = (MySearchFilter, MyOrderingFilter, )
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
