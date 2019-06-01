from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from search.serializers import RelatedTaskSerializer, RelatedServiceSerializer


def get_related_topics_schema():
    operation_description = 'Get a list tasks related to the given topic, sorted by relatedness'
    responses = {
        200: openapi.Response('A list of zero or more related tasks',
                              RelatedTaskSerializer(many=True),
                             ),
        404: 'invalid page',
    }

    return swagger_auto_schema(operation_description=operation_description,
                               responses=responses,
                               )


def get_related_services_schema():
    operation_description = 'Get a list services related to the given topic, sorted by relatedness'
    responses = {
        200: openapi.Response('A list of zero or more related services',
                              RelatedServiceSerializer(many=True),
                             ),
        404: 'invalid page',
    }

    return swagger_auto_schema(operation_description=operation_description,
                               responses=responses,
                               )
