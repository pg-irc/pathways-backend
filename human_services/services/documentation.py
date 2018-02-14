from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

def get_list_schema_decorator():

    taxonomy_term_description = 'Filter result on taxonomic terms, TODO make this take an array of terms with implied logical AND among terms, TODO make this work for hierarchical taxonomies. Examples: "bc211-what:libraries", "bc211-who:service-providers", "bc211-why:homelessness"'

    taxonomy_term_param = openapi.Parameter('taxonomy_term',
                                            openapi.IN_QUERY,
                                            description=taxonomy_term_description,
                                            type=openapi.TYPE_STRING)

    operation_description = 'Return a list of services matching supplied search and filter criteria. Search uses full text search against name and description TODO also against other fields on service and related organization and maybe location.'

    return swagger_auto_schema(operation_description=operation_description,
                               manual_parameters=[taxonomy_term_param])
