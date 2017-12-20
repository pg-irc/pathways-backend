from rest_framework import serializers
from services import models
from locations.serializers import LocationSerializer

class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Service
        fields = ('id', 'name', 'organization_id', 'location_id', 'description')
