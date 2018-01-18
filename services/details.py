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

def raise_404_on_empty(queryset):
    if not queryset.exists():
        raise Http404

def parse_full_text_search_terms(query_parameters):
    query_arguments = query_parameters.get('queries', None)
    if not query_arguments:
        return None
    return query_arguments.split(' ')
