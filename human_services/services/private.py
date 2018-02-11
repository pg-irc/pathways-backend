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

def split_and_strip_if_given(parameter_string):
    if not parameter_string:
        return None
    parameters = parameter_string.split(' ')
    return [p.strip() for p in parameters if p != '']

def parse_sorting(query_parameters):
    sort_argument = query_parameters.get('sort_by', None)
    return split_and_strip_if_given(sort_argument)
