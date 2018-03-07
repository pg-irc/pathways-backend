from django.utils.decorators import method_decorator
from rest_framework import viewsets
from human_services.organizations import models, serializers, documentation

# pylint: disable=too-many-ancestors
@method_decorator(name='list', decorator=documentation.get_organization_list_schema())
class OrganizationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer
