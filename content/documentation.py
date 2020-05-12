from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from content.serializers import AlertSerializer
from common import documentation


def get_alerts_list_schema():
    operation_description = 'Get a list of alerts'
    manual_parameters = ([documentation.get_page_manual_parameter()])
    responses = {
                    200: openapi.Response('A list of zero or more alerts', AlertSerializer(many=True)),
                    404: 'Invalid page',
                }

    return swagger_auto_schema(operation_description=operation_description,
                               manual_parameters=manual_parameters,
                               responses=responses,
                               )
