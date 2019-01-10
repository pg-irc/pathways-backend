from rest_framework import serializers
from human_services.services import models


class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Service
        fields = ('id', 'name', 'organization_id', 'description')
