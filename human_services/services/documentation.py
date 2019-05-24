from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from human_services.services.serializers import ServiceSerializer
from search.serializers import RelatedTopicsForGivenServiceSerializer
from common import documentation
from common.filter_parameter_parsers import TaxonomyParser


def get_service_list_schema():
    operation_description = 'Get a list of services'
    manual_parameters = ([documentation.get_taxonomy_terms_manual_parameter(),
                          documentation.get_page_manual_parameter()])
    responses = {
                    200: openapi.Response('A list of zero or more services', ServiceSerializer(many=True)),
                    400: ', '.join(TaxonomyParser.errors_to_list()),
                    404: 'invalid page',
                }

    return swagger_auto_schema(operation_description=operation_description,
                               manual_parameters=manual_parameters,
                               responses=responses,
                               )


def get_topic_list_schema():
    operation_description = 'Get the list of topics related to a given service'
    manual_parameters = ([])
    responses = {
                    200: openapi.Response('A list of zero or more topics', RelatedTopicsForGivenServiceSerializer(many=True)),
                    404: 'invalid page',
                }

    return swagger_auto_schema(operation_description=operation_description,
                               manual_parameters=manual_parameters,
                               responses=responses,
                               )
