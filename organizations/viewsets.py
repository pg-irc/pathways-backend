from rest_framework import viewsets
from organizations import models, serializers

# pylint: disable=too-many-ancestors
class OrganizationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer
