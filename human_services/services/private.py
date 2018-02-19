from django.core.exceptions import SuspiciousOperation

def parse_taxonomy_parameter(query_parameters):
    parameter = query_parameters.get('taxonomy_term', None)
    if not parameter:
        return None
    split_terms = [term.split(':') for term in parameter.split(',')]
    return [build_valid_taxonomy_parameters(split_term) for split_term in split_terms]

def build_valid_taxonomy_parameters(taxonomy_term):
    if len(taxonomy_term) != 2:
        raise_taxonomy_error()
    taxonomy_id, term = taxonomy_term
    if not taxonomy_id or not term:
        raise_taxonomy_error()
    return (taxonomy_id, term)

def raise_taxonomy_error():
    raise SuspiciousOperation('Invalid argument to taxonomy_term')

def add_taxonomy_filter_if_given(queryset, search_parameters):
    taxonomy_terms = search_parameters.taxonomy_terms
    if not taxonomy_terms:
        return queryset

    for term in taxonomy_terms:
        queryset = queryset.filter(taxonomy_terms__taxonomy_id=term[0],
                                   taxonomy_terms__name=term[1])
    return queryset

def add_organization_filter_if_given(queryset, search_parameters):
    if search_parameters.organization_id:
        queryset = queryset.filter(organization_id=search_parameters.organization_id)
    return queryset

def add_location_filter_if_given(queryset, search_parameters):
    if search_parameters.location_id:
        queryset = queryset.filter(serviceatlocation__location_id=search_parameters.location_id)
    return queryset
