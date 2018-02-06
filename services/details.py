from django.core.exceptions import SuspiciousOperation
from django.http import Http404

def parse_taxonomy_parameter(query_parameters):
    taxonomy_term = query_parameters.get('taxonomy_term', None)
    return build_valid_taxonomy_parameters(taxonomy_term)

def build_valid_taxonomy_parameters(taxonomy_term):
    if not taxonomy_term:
        return None, None
    if taxonomy_term.count(':') != 1:
        raise_taxonomy_error()
    taxonomy_id, term = taxonomy_term.split(':')
    if not taxonomy_id or not term:
        raise_taxonomy_error()
    return taxonomy_id, term

def raise_taxonomy_error():
    raise SuspiciousOperation('Invalid argument to taxonomy_term')

def parse_full_text_search_terms(query_parameters):
    search_argument = query_parameters.get('search', None)
    return split_and_strip_if_given(search_argument)

def split_and_strip_if_given(parameter_string):
    if not parameter_string:
        return None
    parameters = parameter_string.split(' ')
    return [p.strip() for p in parameters if p != '']


class FilterBuilder:
    def __init__(self):
        self.filter = None

    def add_with_or(self, *filters):
        new_filters = self.join_with_or(*filters)
        self.filter = self.join_with_and(self.filter, new_filters)

    @staticmethod
    def join_with_and(*filters):
        result = None
        for filter in filters:
            if result:
                result = result & filter
            else:
                result = filter
        return result

    @staticmethod
    def join_with_or(*filters):
        result = None
        for filter in filters:
            if result:
                result = result | filter
            else:
                result = filter
        return result

    def get_filter(self):
        return self.filter


def parse_sorting(query_parameters):
    sort_argument = query_parameters.get('sort_by', None)
    return split_and_strip_if_given(sort_argument)
