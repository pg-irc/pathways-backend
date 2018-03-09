from rest_framework import serializers
from human_services.locations import models


class ServiceAtLocationSerializer(serializers.ModelSerializer):
    service_name = serializers.ReadOnlyField(source='service.name')
    location_name = serializers.ReadOnlyField(source='location.name')

    class Meta:
        model = models.ServiceAtLocation
        fields = ('service_name', 'location_name')
