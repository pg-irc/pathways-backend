from rest_framework import filters

REVERSE_PREFIX = '-'

class OrderingFilter(filters.OrderingFilter):
    ordering_description = 'Fields for sorting of results. Enter one or more fields separated by space or comma. Prefix any field with - for sorting in descending order.'

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


class SearchFilter(filters.SearchFilter):
    search_description = 'Search terms for full text search. Enter one or more terms separated by space or comma. Logical AND is implied among the terms.'
