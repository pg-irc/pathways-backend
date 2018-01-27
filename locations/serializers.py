from rest_framework import serializers
from locations import models
from addresses.serializers import AddressSerializer


class LocationAddressSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    class Meta:
        model = models.LocationAddress
        fields = ('address_type', 'address')


class LocationSerializer(serializers.ModelSerializer):
    location_addresses = LocationAddressSerializer(many=True)
    class Meta:
        model = models.Location
        fields = ('id', 'name', 'organization_id', 'latitude',
                  'longitude', 'location_addresses', 'description')
