from rest_framework import serializers
from qa_tool import models


class RelevancyScoreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.RelevancyScore
        fields = ('id', 'value', 'time_stamp', 'algorithm_id',
                  'search_location_id', 'user_id', 'service_at_location_id')


class AlgorithmSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Algorithm
        fields = ('id', 'url', 'name', 'notes')


class SearchLocationSerializer(serializers.HyperlinkedModelSerializer):
    latitude = serializers.ReadOnlyField(source='point.y')
    longitude = serializers.ReadOnlyField(source='point.x')

    class Meta:
        model = models.SearchLocation
        fields = ('id', 'name', 'latitude', 'longitude')
