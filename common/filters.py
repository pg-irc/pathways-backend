from rest_framework import filters
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from common.filter_parameter_parsers import ProximityParser


class MultiFieldOrderingFilter(filters.OrderingFilter):
    REVERSE_SORT_PREFIX = '-'
    ordering_description = ('Fields for sorting of results. Enter one or more fields separated '
                            'by space or comma. Records that sort equally by the first field are '
                            'sorted by the second field, etc. Prefix any field with '
                            + REVERSE_SORT_PREFIX + ' for sorting in descending order.')

    def get_ordering(self, request, queryset, view):
        argument_string = request.query_params.get(self.ordering_param)
        if argument_string:
            arguments = argument_string.replace(',', ' ').split()
            return (self.set_prefix(argument) for argument in arguments if argument)
        return None

    def set_prefix(self, argument):
        argument = argument.strip()
        reverse_sort = argument[0:1] == self.REVERSE_SORT_PREFIX
        stripped_argument = argument[1:] if reverse_sort else argument

        translated_fields = ['name', 'description']
        if stripped_argument not in translated_fields:
            return argument

        argument = 'translations__' + stripped_argument
        return self.REVERSE_SORT_PREFIX + argument if reverse_sort else argument


class SearchFilter(filters.SearchFilter):
    search_description = ('Search terms for full text search. Enter one or more terms separated '
                          'by space or comma. Logical AND is implied among the terms. TODO '
                          'currently only looks in name and description, make it look more '
                          'widely.')


class ProximityFilter(filters.BaseFilterBackend):
    filter_description = ('Order by proximity to a point. '
                          'Accepts two comma separated values representing a latitude and a longitude. '
                          'Example: "proximity=+49.2827,-123.1207".')
    srid = 4326

    def filter_queryset(self, request, queryset, view):
        query_parameters = request.query_params
        path_parameters = view.kwargs
        proximity = ProximityParser.parse_proximity(query_parameters.get('proximity', None))
        if proximity:
            queryset = (queryset
                        .annotate(distance=Distance('location__point', Point(proximity, srid=self.srid)))
                        .order_by('distance'))
        location_id = path_parameters.get('location_id', None)
        if location_id:
            queryset = queryset.filter(location_id=location_id)
        service_id = path_parameters.get('service_id', None)
        if service_id:
            queryset = queryset.filter(service_id=service_id)
        return queryset
