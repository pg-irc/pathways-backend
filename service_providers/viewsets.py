from rest_framework import viewsets
from service_providers import models, serializers

class ServiceProviderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.ServiceProvider.objects.all()
    serializer_class = serializers.ServiceProviderSerializer
