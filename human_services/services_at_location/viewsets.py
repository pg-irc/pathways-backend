from rest_framework import viewsets
from django.utils.decorators import method_decorator
from human_services.locations import models
from human_services.services_at_location import documentation, serializers
from common.filters import (ProximityFilter, SearchFilter, LocationIdFilter,
                            ServiceIdFilter, TaxonomyFilter)


# pylint: disable=too-many-ancestors
@method_decorator(name='list', decorator=documentation.get_service_at_location_list_schema())
class ServiceAtLocationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.ServiceAtLocation.objects.all()
    serializer_class = serializers.ServiceAtLocationSerializer
    search_fields = ('location__translations__name', 'location__translations__description',
                     'service__translations__name', 'service__translations__description')
    filter_backends = (ProximityFilter,
                       SearchFilter,
                       LocationIdFilter,
                       ServiceIdFilter,
                       TaxonomyFilter,)
