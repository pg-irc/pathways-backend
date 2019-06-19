from rest_framework import viewsets
from django.utils.decorators import method_decorator
from human_services.locations import models, serializers, documentation
from common.filters import (ProximitySortFilter, SearchFilter, LocationIdFilter,
                            ServiceIdFilter, TaxonomyFilter)

# pylint: disable=too-many-ancestors
@method_decorator(name='list', decorator=documentation.get_location_list_schema())
class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Location.objects.all()
    serializer_class = serializers.LocationSerializer


# pylint: disable=too-many-ancestors
class LocationViewSetUnderOrganizations(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        organization_id = self.kwargs['organization_id']
        return models.Location.objects.filter(organization=organization_id)

    serializer_class = serializers.LocationSerializer
