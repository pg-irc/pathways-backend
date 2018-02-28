from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from human_services.locations.serializers import ServiceAtLocationSerializer
from common.filters import ProximityFilter, TaxonomyFilter
from common.filter_parameter_parsers import ProximityParameterParser, TaxonomyParameterParser

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
                         # TODO come up with a strategy to not duplicate from documentation in services app
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
                    200: openapi.Response('A list of zero or more services at locations', ServiceAtLocationSerializer(many=True)),
                    400: (', '.join([ProximityParameterParser.errors_to_string(),
                          TaxonomyParameterParser.errors_to_string()])),
                    404: 'Invalid page',
                }

    return swagger_auto_schema(operation_description=operation_description,
                               manual_parameters=manual_parameters,
                               responses=responses,
                               )
