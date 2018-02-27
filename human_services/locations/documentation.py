from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from human_services.locations.serializers import ServiceAtLocationSerializer
from common.filters import ProximityFilter
from common.filter_parameter_parsers import ProximityParser

def get_list_schema_decorator():

    operation_description = 'Get a list of services at locations'

    manual_parameters = [openapi.Parameter('proximity',
                                            openapi.IN_QUERY,
                                            description=ProximityFilter.filter_description,
                                            type=openapi.TYPE_STRING,
                                            # Regex representing a latitude and longitude.
                                            # Valid patterns consist of two integers or floats, comma separated, with
                                            # optional + or - prefixes. One space after the comma is allowed here.
                                            pattern=r'^[-+]?[0-9]+\.?[0-9]*,\s?[-+]?[0-9]+\.?[0-9]*$'),
                        ]

    responses = {
                    200: openapi.Response('A list of zero or more services at locations', ServiceAtLocationSerializer(many=True)),
                    400: ProximityParser.errors_to_string(),
                    404: 'Invalid page',
                }

    return swagger_auto_schema(operation_description=operation_description,
                               manual_parameters=manual_parameters,
                               responses=responses,
                               )
