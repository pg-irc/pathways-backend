from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from human_services.locations.serializers import ServiceAtLocationSerializer
from common.documentation import ManualParameters
from common.filter_parameter_parsers import ProximityParser, TaxonomyParser

def get_list_schema_decorator():
    operation_description = 'Get a list of services at locations'
    manual_parameters = [ManualParameters.get_taxonomy_terms_parameter()]
    responses = {
                    200: openapi.Response('A list of zero or more services at locations', ServiceAtLocationSerializer(many=True)),
                    400: (', '.join([ProximityParser.errors_to_string(),
                          TaxonomyParser.errors_to_string()])),
                    404: 'Invalid page',
                }

    return swagger_auto_schema(operation_description=operation_description,
                               manual_parameters=manual_parameters,
                               responses=responses,
                               )
