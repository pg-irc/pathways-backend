from rest_framework import viewsets
from services import models, serializers

# pylint: disable=too-many-ancestors
class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        queryset = models.Service.objects.all()
        taxonomy_term = self.request.query_params.get('taxonomy_term', None)
        if taxonomy_term:
            taxonomy, term = self.parse_taxonomy_term_argument(taxonomy_term)
            queryset = (queryset.
                            filter(taxonomy_terms__name=term).
                            filter(taxonomy_terms__taxonomy_id=taxonomy))
        return queryset

    def parse_taxonomy_term_argument(self, term):
        return term.split(':')

    serializer_class = serializers.ServiceSerializer

# pylint: disable=too-many-ancestors
class ServiceViewSetUnderOrganizations(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        organization_id = self.kwargs['organization_id']
        return models.Service.objects.filter(organization=organization_id)

    serializer_class = serializers.ServiceSerializer
