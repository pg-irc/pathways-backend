from rest_framework import viewsets
from django.utils.decorators import method_decorator
from human_services.services import models, serializers, documentation
from common.filters import (SearchFilter, OrganizationIdFilter, LocationIdFilter,
                            TaxonomyFilter, MultiFieldOrderingFilter)
from search.models import TaskServiceSimilarityScore
from search.serializers import RelatedServiceSerializer

# pylint: disable=too-many-ancestors
@method_decorator(name='list', decorator=documentation.get_service_list_schema())
class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceSerializer
    search_fields = ('translations__name', 'translations__description',)
    filter_backends = (MultiFieldOrderingFilter, SearchFilter, OrganizationIdFilter,
                       LocationIdFilter, TaxonomyFilter,)
    ordering_fields = '__all__'


class ServiceTopicsViewSet(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        service_id = self.kwargs['service_id']
        return (TaskServiceSimilarityScore.objects.
                filter(service=service_id).
                order_by('-similarity_score'))

    serializer_class = RelatedServiceSerializer
