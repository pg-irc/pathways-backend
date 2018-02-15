from django.core.exceptions import SuspiciousOperation

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

def add_taxonomy_filter_if_given(queryset, search_parameters):
    identifier = search_parameters.taxonomy_id
    term = search_parameters.taxonomy_term
    if identifier and term:
        queryset = queryset.filter(taxonomy_terms__taxonomy_id=identifier,
                                   taxonomy_terms__name=term)
    return queryset

def add_organization_filter_if_given(queryset, search_parameters):
    if search_parameters.organization_id:
        queryset = queryset.filter(organization_id=search_parameters.organization_id)
    return queryset

def add_location_filter_if_given(queryset, search_parameters):
    if search_parameters.location_id:
        queryset = queryset.filter(serviceatlocation__location_id=search_parameters.location_id)
    return queryset
