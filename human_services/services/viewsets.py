from rest_framework import viewsets
from rest_framework.schemas.inspectors import AutoSchema
import coreapi, coreschema
from human_services.services import models, serializers
from . import private

def get_auto_schema_for_service_endpoint():
    # TODO this is for list only!!!
    return AutoSchema(manual_fields=[
        coreapi.Field(
            'search',
            location='query',
            description='Search terms for full text search in all fields int the service record and related location and organization records, logical AND implied among terms',
            schema=coreschema.Array(items=coreschema.String())
        ),
        coreapi.Field(
            'taxonomy_term',
            location='query',
            description='Filter result on taxonomic terms, TODO make this take an array of terms with implied logical AND among terms, TODO make this work for hierarchical taxonomies',
            schema=coreschema.String(pattern='\w+:\w+')
        ),
        coreapi.Field(
            'sort_by',
            location='query',
            description='Sort resulting services by one or more fields, prefix field name with - for descending sort order, records that sort equal by the first term are sorted by the second term, etc.',
            schema=coreschema.Array(items=coreschema.String())
        ),
    ])

class SearchParameters:
    def __init__(self, query_parameters):
        self.taxonomy_id, self.taxonomy_term = private.parse_taxonomy_parameter(query_parameters)
        self.full_text_search_terms = private.parse_full_text_search_terms(query_parameters)
        self.sort_by = private.parse_sorting(query_parameters)

# pylint: disable=too-many-ancestors
class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    schema = get_auto_schema_for_service_endpoint()

    def get_queryset(self):
        query_parameters = self.request.query_params
        search_parameters = SearchParameters(query_parameters)
        queryset = models.Service.get_queryset(search_parameters)
        return queryset

    serializer_class = serializers.ServiceSerializer

# pylint: disable=too-many-ancestors
class ServiceViewSetUnderOrganizations(viewsets.ReadOnlyModelViewSet):
    schema = get_auto_schema_for_service_endpoint()

    def get_queryset(self):
        organization_id = self.kwargs['organization_id']
        return models.Service.objects.filter(organization=organization_id)

    serializer_class = serializers.ServiceSerializer
