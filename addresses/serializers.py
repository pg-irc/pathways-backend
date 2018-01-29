from rest_framework import serializers
from addresses import models


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Address
        fields = ('id', 'attention', 'address', 'city',
                  'state_province', 'postal_code', 'country')


class AddressTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AddressType
        fields = ('id')
