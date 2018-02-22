from rest_framework import filters
from rest_framework.exceptions import ParseError
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance


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


class BaseProximityFilter(filters.BaseFilterBackend):
    filter_parameter = 'proximity'
    filter_description = ('Order by proximity to a point. '
                          'Accepts two comma separated values representing a latitude and a longitude. '
                          'Example: "{0}=+49.2827,-123.1207".'.format(filter_parameter))
    parse_errors = [
        'Exactly two comma separated values expected for {0}'.format(filter_parameter),
        'Values provided to {0} must be able to represent integers'.format(filter_parameter),
    ]
    srid = 4326

    def get_model_point_field(self):
        raise NotImplementedError('.get_model_point_field() must be overridden.')

    def get_reference_point(self, request):
        parameters = request.query_params.get(self.filter_parameter)
        if parameters:
            latitude_longitude_values = [parameter.strip() for parameter in parameters.split(',')]
            latitude_longitude_length = 2
            if (len(latitude_longitude_values) != latitude_longitude_length):
                raise (ParseError(self.parse_errors[0]))
            try:
                latitude = float(latitude_longitude_values[0])
                longitude = float(latitude_longitude_values[1])
            except ValueError:
                raise (ParseError(self.parse_errors[1]))
            return Point(latitude, longitude, srid=self.srid)
        return None

    def filter_queryset(self, request, queryset, view):
        reference_point = self.get_reference_point(request)
        if reference_point:
            model_point_field = self.get_model_point_field()
            return (queryset
                    .annotate(distance=Distance(model_point_field, reference_point))
                    .order_by('distance'))
        return queryset


class ServiceAtLocationProximityFilter(BaseProximityFilter):
    def get_model_point_field(self):
        return 'location__point'
