from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from human_services.services.serializers import ServiceSerializer
from common.filters import TaxonomyFilter
from common.filter_parameter_parsers import TaxonomyParameterParser

def get_list_schema_decorator():

    operation_description = 'Get a list of services'

    page_description = ('A page number within the paginated result set. When returning a paginated '
                        'result, the response contains a Count header with the total number of '
                        'entries in the result, and a Link header with links to first, prev, next '
                        'and last pages in the result')

    manual_parameters = [openapi.Parameter('page',
                                           openapi.IN_QUERY,
                                           description=page_description,
                                           type=openapi.TYPE_INTEGER),
                         openapi.Parameter('taxonomy_terms',
                                           openapi.IN_QUERY,
                                           description=TaxonomyFilter.filter_description,
                                           type=openapi.TYPE_STRING,
                                           # One term followed by comma and additional terms zero or more times,
                                           # where a term consits of one or more letters/dashes, a dot, and more
                                           # letters/dashes. White space is allowed around the comma but not the
                                           # dots
                                           pattern=r'^[\w\-]+\.[\w\-]+(\W*,\W*[\w\-]+\.[\w\-]+)*$'),
                        ]

    responses = {
                    200: openapi.Response('A list of zero or more services', ServiceSerializer(many=True)),
                    400: TaxonomyParameterParser.errors_to_string(),
                    404: 'invalid page',
                }

    return swagger_auto_schema(operation_description=operation_description,
                               manual_parameters=manual_parameters,
                               responses=responses,
                               )
