from rest_framework import serializers
from human_services.services import models

class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    location_id = serializers.SerializerMethodField('service_location_id')

    class Meta:
        model = models.Service
        fields = ('id', 'name', 'organization_id', 'location_id', 'description')

    def service_location_id(self, service):
        location = self.service_at_location(service)
        return location.id if location else None

    def service_at_location(self, service):
        return service.locations.first()
