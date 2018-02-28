from rest_framework import viewsets
from django.utils.decorators import method_decorator
from human_services.services import models, serializers, documentation
from common.filters import (SearchFilter, OrganizationIdFilter, LocationIdFilter,
                            TaxonomyFilter, MultiFieldOrderingFilter)


# pylint: disable=too-many-ancestors
@method_decorator(name='list', decorator=documentation.get_list_schema_decorator())
class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceSerializer
    search_fields = ('translations__name', 'translations__description',)
    filter_backends = (MultiFieldOrderingFilter, SearchFilter, OrganizationIdFilter,
                       LocationIdFilter, TaxonomyFilter,)
    ordering_fields = '__all__'
