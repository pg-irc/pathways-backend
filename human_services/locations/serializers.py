from rest_framework import serializers
from human_services.locations import models
from human_services.addresses.serializers import AddressSerializer


class LocationAddressSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    class Meta:
        model = models.LocationAddress
        fields = ('address_type', 'address')


class LocationSerializer(serializers.ModelSerializer):
    location_addresses = LocationAddressSerializer(many=True)
    latitude = serializers.ReadOnlyField(source='point.x')
    longitude = serializers.ReadOnlyField(source='point.y')

    class Meta:
        model = models.Location
        fields = ('id', 'name', 'organization_id', 'latitude',
                  'longitude', 'location_addresses', 'description')


class ServiceAtLocationSerializer(serializers.ModelSerializer):
    service_name = serializers.ReadOnlyField(source='service.name')
    location_name = serializers.ReadOnlyField(source='location.name')

    class Meta:
        model = models.ServiceAtLocation
        fields = ('service_name', 'location_name')
