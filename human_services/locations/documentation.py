from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema
from human_services.locations.serializers import LocationSerializer
from common import documentation


def get_location_list_schema():
    operation_description = 'Get a list of locations'
    manual_parameters = ([documentation.get_page_manual_parameter()])
    responses = {
        200: openapi.Response('A list of zero or more locations', LocationSerializer(many=True)),
        404: 'Invalid page',
    }

    return swagger_auto_schema(operation_description=operation_description,
                               manual_parameters=manual_parameters,
                               responses=responses,
                               )
