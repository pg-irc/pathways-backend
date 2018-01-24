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
    query_arguments = query_parameters.get('search', None)
    if not query_arguments:
        return None
    search_terms = query_arguments.split(' ')
    return [x.strip() for x in search_terms if x != '']


class FilterBuilder:
    def __init__(self):
        self.filter = None

    def add_with_or(self, *filters):
        new_filters = self.join_with_or(*filters)
        self.filter = self.join_with_and(self.filter, new_filters)

    def join_with_and(self, *filters):
        result = None
        for filter in filters:
            result = result & filter if result else filter
        return result

    def join_with_or(self, *filters):
        result = None
        for filter in filters:
            result = result | filter if result else filter
        return result

    def get_filter(self):
        return self.filter


def parse_sorting_and_paging(query_parameters):
    sort_arguments = query_parameters.get('sort_by', None)
    if sort_arguments:
        sort_terms = sort_arguments.split(' ')
        sort_arguments = [x.strip() for x in sort_terms if x != '']

    per_page = query_parameters.get('per_page', None)
    if per_page:
        per_page = int(per_page) if per_page else None

    page = query_parameters.get('page', None)
    if page:
        page = int(page) if page else None

    return sort_arguments, per_page, page
