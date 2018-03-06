from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from human_services.services.serializers import ServiceSerializer
from common import documentation
from common.filter_parameter_parsers import TaxonomyParser

def get_list_schema_decorator():
    operation_description = 'Get a list of services'
    page_description = ('A page number within the paginated result set. When returning a paginated '
                        'result, the response contains a Count header with the total number of '
                        'entries in the result, and a Link header with links to first, prev, next '
                        'and last pages in the result')
    manual_parameters = ([documentation.get_proximity_manual_parameter(),
                          documentation.get_taxonomy_terms_manual_parameter()])
    responses = {
                    200: openapi.Response('A list of zero or more services', ServiceSerializer(many=True)),
                    400: ', '.join(TaxonomyParser.errors_to_list()),
                    404: 'invalid page',
                }

    return swagger_auto_schema(operation_description=operation_description,
                               manual_parameters=manual_parameters,
                               responses=responses,
                               )
