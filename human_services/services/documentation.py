from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from human_services.services.serializers import ServiceSerializer

def get_list_schema_decorator():

    operation_description = 'Get a list of services'

    taxonomy_description = ('Filter result on taxonomic terms, specify one or more terms of the '
                            'form taxonomy$term. Examples: "bc211-what$libraries", '
                            '"bc211-who$service-providers", "bc211-why$homelessness". '
                            'If more than one term is given, records returned are those that are '
                            'annotated with all specified terms. TODO make this work for '
                            'hierarchical taxonomies.')

    manual_parameters = [openapi.Parameter('taxonomy_terms',
                                           openapi.IN_QUERY,
                                           description=taxonomy_description,
                                           type=openapi.TYPE_STRING,
                                           pattern=r'\w+\$\w+'),
                        ]

    responses = {
                    200: openapi.Response('a service', ServiceSerializer),
                    400: 'invalid taxonomy term format, invalid field for sorting',
                    404: 'invalid page',
                }

    return swagger_auto_schema(operation_description=operation_description,
                               manual_parameters=manual_parameters,
                               responses=responses,
                               )
