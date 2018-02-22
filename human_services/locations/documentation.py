from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from human_services.locations.serializers import ServiceAtLocationSerializer
from common.filters import ServiceAtLocationProximityFilter

def get_list_schema_decorator():

    operation_description = 'Get a list of services at locations'

    manual_parameters = [openapi.Parameter('proximity',
                                            openapi.IN_QUERY,
                                            description=ServiceAtLocationProximityFilter.filter_description,
                                            type=openapi.TYPE_STRING,
                                            # Regex representing a latitude and longitude.
                                            # Valid patterns consist of two integers or floats, comma separated, with
                                            # optional + or - prefixes.
                                            pattern=r'[-+]?[0-9]+\.?[0-9]*,[-+]?[0-9]+\.?[0-9]*'),
                        ]

    responses = {
                    200: openapi.Response('A list of zero or more services at locations', ServiceAtLocationSerializer(many=True)),
                    400: ', '.join(ServiceAtLocationProximityFilter.parse_errors),
                    404: 'Invalid page',
                }

    return swagger_auto_schema(operation_description=operation_description,
                               manual_parameters=manual_parameters,
                               responses=responses,
                               )
