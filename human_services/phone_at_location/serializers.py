from rest_framework import serializers
from human_services.phone_at_location import models


class PhoneAtLocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PhoneAtLocation
        fields = ('phone_number_type', 'phone_number')
