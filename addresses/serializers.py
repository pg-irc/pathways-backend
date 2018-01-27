from rest_framework import serializers
from addresses import models


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Address
        fields = ('id', 'address', 'city', 'country',
                  'attention', 'state_province', 'postal_code')


class AddressTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AddressType
        fields = ('id')
