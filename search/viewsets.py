from rest_framework import viewsets
from rest_framework.response import Response

from organizations.models import Organization
from organizations.serializers import OrganizationSerializer

class SearchViewSet(viewsets.GenericViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    def get_queryset(self):
        return Organization.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        organizations_serializer = OrganizationSerializer(queryset, many=True)
        return Response({
            'organizations': organizations_serializer.data,
            'locations': [],
            'services': [],
        })
